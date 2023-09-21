import numpy as np
import plotly.graph_objects as go
import math

class StepsError(Exception):
    def __init__(self, message):
        super().__init__(message)

class xIntervalError(Exception):
    def __init__(self, message):
        super().__init__(message)

class yIntervalError(Exception):
    def __init__(self, message):
        super().__init__(message)

class DimensionError(Exception):
    def __init__(self, message):
        super().__init__(message)

class FramesError(Exception):
    def __init__(self, message):
        super().__init__(message)

def do_fxy_plot(formula,xstart,xend,ystart,yend,step,colorscale='Electric',title=None,xtitle='X-axis',ytitle='Y-axis',ztitle='Z-axis'):
    """
    This function takes a string and evaluates it as a function of x and y i.e. f(x,y) and plots a graph for the function.
    Args:
        ----Required Arguments----
        formula (string): formula in terms of x and y for the function f(x,y)
        xstart (float): starting extreme of x value to evaluate f(x,y) from
        xend (float): ending extreme of x value to evaluate f(x,y) to
        ystart (float): starting extreme of y value to evaluate f(x,y) from
        yend (float): ending extreme of y value to evaluate f(x,y) to
        step (float): incrementation to continuously evaluate f(x,y) with i.e. (x +/- step, y +/- step)
        ----Optional Arguments----
        colorscale (string): Default 'Electric', can be any of the following (Blackbody, Bluered, Blues, C ividis,
        Earth, Electric, Greens, Greys, Hot, Jet, Picnic, Portland, Rainbow, RdBu, Reds, Viridis, YlGnBu, YlOrRd)
        title (string): Default to the formula parameter, title of the plot
        xtitle (string): Default to 'X-axis', x-axis title
        ytitle (string): Default to 'Y-axis', y-axis title
        ztitle (string): Default to 'Z-axis', z-axis title
    Returns:
        plotly.graph_objects.Figure
    Raises:
        StepsError: step must be higher than 0
        xIntervalError: xend is lesser than xstart
        yIntervalError: yend is lesser than ystart
        Other Errors such as invalid evaluation
        wrong argument passed as colorscale
    Note:
        [Assuming the output is given to a variable fig]
        The graph can be shown using the output with fig.show()
        The graph can be further modified using fig.update_layout, refer here: https://plotly.com/python/reference/layout/
    """
    try:
        if title == None:
            title = formula
        if(step <= 0):
            raise StepsError("step must be higher than 0")
        if(xstart > xend):
            raise xIntervalError("xstart must be lesser than xend")
        if(ystart > yend):
            raise yIntervalError("ystart must be lesser than yend")
        xlist = []
        ylist = []
        zlist = []
        while xstart <= xend:
            ty = ystart
            while ystart <= yend:
                try:
                    z = eval(formula, {"x": xstart, "y": ystart,"math": math})
                except ZeroDivisionError:
                    z = np.nan
                zlist.append(z)
                xlist.append(xstart)
                ylist.append(ystart)
                ystart += step
            ystart = ty
            xstart += step
        num = len(xlist)
        sq = math.sqrt(num)
        sq = int(sq)
        while num % sq != 0:
            sq -= 1
        xlist = np.array(xlist).reshape((sq, int(num/sq)))
        ylist = np.array(ylist).reshape((sq, int(num/sq)))
        zlist = np.array(zlist).reshape((sq, int(num/sq)))
        fig = go.Figure(data=[go.Surface(z=zlist, x=xlist, y=ylist, colorscale=colorscale)])
        fig.update_layout(
            title = title,
            scene=dict(
                xaxis_title=xtitle,
                yaxis_title=ytitle,
                zaxis_title=ztitle
            )
        )
        return fig
    except Exception as error:
        print(f"An error occured: {error}")
        return None

def do_fx_plot(formula,xstart,xend,step,color='lime',width=2,title=None,xtitle='X-axis',ytitle='Y-axis'):
    """
    This function takes a string and evaluates it as a function of x i.e. f(x) and plots a graph for the function.
    Args:
        ----Required Arguments----
        formula (string): formula in terms of x and y for the function f(x)
        xstart (float): starting extreme of x value to evaluate f(x) from
        xend (float): ending extreme of x value to evaluate f(x) to
        step (float): incrementation to continuously evaluate f(x) with i.e. (x +/- step)
        ----Optional Arguments----
        color (string): Default 'lime'
        width (float): Default 2, width of the curve
        title (string): Default to the formula parameter, title of the plot
        xtitle (string): Default to 'X-axis', x-axis title
        ytitle (string): Default to 'Y-axis', y-axis title
    Returns:
        plotly.graph_objects.Figure
    Raises:
        StepsError: step must be higher than 0
        xIntervalError: xend is lesser than xstart
        Other Errors such as invalid evaluation
        wrong argument passed as colorscale
    Note:
        [Assuming the output is given to a variable fig]
        The graph can be shown using the output with fig.show()
        The graph can be further modified using fig.update_layout, refer here: https://plotly.com/python/reference/layout/
    """
    try:
        if title == None:
            title = formula
        if(step <= 0):
            raise StepsError("step must be higher than 0")
        if(xstart > xend):
            raise xIntervalError("xstart must be lesser than xend")
        xlist = []
        ylist = []
        while xstart <= xend:
            y = None
            try:
                y = eval(formula, {"x": xstart,"math": math})
            except:
                y = np.nan
            xlist.append(xstart)
            ylist.append(y)
            xstart += step
        xlist = np.array(xlist)
        ylist = np.array(ylist)
        fig = go.Figure(data=[go.Scatter(x=xlist, y=ylist, mode='lines', line=dict(width=width,color=color),name='F(x)',showlegend=True)])
        fig.update_layout(
            title = title,
            xaxis_title=xtitle,
            yaxis_title=ytitle,
        )
        return fig
    except Exception as error:
        print(f"An error occured: {error}")
        return None

def animate_xy_particles(x,y,size=7,colors=None,title=None):
    """
    This function takes a set of particles and animates its movements
    Args:
        ----Required Arguments----
        x (list): A list of list of x coordinates of n particles for iterations equal to number of rows.
        y (list): A list of list of y coordinates of n particles for iterations equal to number of rows.
        ----Optional Arguments----
        size (float): Default size is 7, size of particles.
        colors (list): Default all particles are colored 'steelblue', a list of strings with n colors.
        title (string): Title of the plot
    Returns:
        plotly.graph_objects.Figure
    Raises:
        DimensionError: x and y list don't have the same dimensions
        
        Other Errors such as invalid evaluation
        wrong argument passed as colors
    Note:
        [Assuming the output is given to a variable fig]
        The graph can be shown using the output with fig.show()
        The graph can be further modified using fig.update_layout, refer here: https://plotly.com/python/reference/layout/
    """  
    try:
        if title == None:
            title = "Animated Particles"
        if colors == None:
            colors = "steelblue"
        minx = None
        maxx = None
        miny = None
        maxy = None
        if len(x) != len(y):
            raise DimensionError("x and y list don't have the same dimensions")
        cons = len(x[0])
        for i in range(0,len(x)):
            if len(x[i]) != len(y[i]) or len(x[i]) != cons:
                raise DimensionError("x and y lists don't have the same dimensions")
        for i in range(0,len(x)):
            for j in range(0,len(x[0])):
                if minx == None:
                    minx = x[i][j]
                else:
                    minx = min(minx,x[i][j])
                if maxx == None:
                    maxx = x[i][j]
                else:
                    maxx = max(maxx,x[i][j])
                if miny == None:
                    miny = y[i][j]
                else:
                    miny = min(miny,y[i][j])
                if maxy == None:
                    maxy = y[i][j]
                else:
                    maxy = max(maxy,y[i][j])
        fig = go.Figure(
            data=[go.Scatter(x=x[0], y=y[0],
                             mode="markers",
                             marker=dict(color=colors, size=size),
                             showlegend=False)
                 ],
            layout=go.Layout(
                        title_text=title,
                        hovermode="closest",
                        xaxis_title="X-Coordinates",
                        yaxis_title="Y-Coordinates",
                        xaxis=dict(range=[minx-1,maxx+1], autorange=False, zeroline=False),
                        yaxis=dict(range=[miny-1,maxy+1], autorange=False, zeroline=False),
                        updatemenus=[dict(type="buttons",
                                          buttons=[dict(label="Play",
                                                        method="animate",
                                                        args=[None])]
                                         )
                                    ]
                        ),
            frames=[go.Frame(
                        data=[go.Scatter(
                        x=x[i],
                        y=y[i],
                        mode="markers",
                        marker=dict(color=colors, size=size),name='Particles',showlegend=True)])
                    for i in range(0,len(x))]
        )
        return fig
    except Exception as error:
        print(f"An error occured: {error}")
        return
    
def animate_xyz_particles(x,y,z,size=7,colors=None,title=None,framespmov=10):
    """
    This function takes a set of particles and animates its movements
    Args:
        ----Required Arguments----
        x (list): A list of list of x coordinates of n particles for iterations equal to number of rows.
        y (list): A list of list of y coordinates of n particles for iterations equal to number of rows.
        z (list): A list of list of z coordinates of n particles for iterations equal to number of rows.
        ----Optional Arguments----
        size (float): Default size is 7, size of particles.
        colors (list): Default all particles are colored 'steelblue', a list of strings with n colors.
        title (string): Title of the plot
        framespmov (int): Default value is 10, Frames for movement from one position to another, must be greater than 1.
    Returns:
        plotly.graph_objects.Figure
    Raises:
        DimensionError: x, y, and z lists don't have the same dimensions
        FramesError: framespmov should be greater or equal to 1
        Other Errors such as invalid evaluation
        wrong argument passed as colors
    Note:
        [Assuming the output is given to a variable fig]
        The graph can be shown using the output with fig.show()
        The graph can be further modified using fig.update_layout, refer here: https://plotly.com/python/reference/layout/
    """
    try:
        framespmov = int(framespmov)
        if title is None:
            title = "Animated Particles"
        if colors is None:
            colors = "steelblue"
        if framespmov <= 0:
            raise FramesError("framespmov should be greater or equal to 1")
        minx = None
        maxx = None
        miny = None
        maxy = None
        minz = None
        maxz = None
        if len(x) != len(y) or len(x) != len(z):
            raise DimensionError("x, y, and z lists don't have the same dimensions")
        cons = len(x[0])
        for i in range(0, len(x)):
            if len(x[i]) != len(y[i]) or len(x[i]) != cons or len(x[i]) != len(z[i]):
                raise DimensionError("x, y, and z lists don't have the same dimensions")
        for i in range(0, len(x)):
            for j in range(0, len(x[0])):
                if minx == None:
                    minx = x[i][j]
                else:
                    minx = min(minx, x[i][j])
                if maxx == None:
                    maxx = x[i][j]
                else:
                    maxx = max(maxx, x[i][j])
                if miny == None:
                    miny = y[i][j]
                else:
                    miny = min(miny, y[i][j])
                if maxy == None:
                    maxy = y[i][j]
                else:
                    maxy = max(maxy, y[i][j])
                if minz == None:
                    minz = z[i][j]
                else:
                    minz = min(minz, z[i][j])
                if maxz == None:
                    maxz = z[i][j]
                else:
                    maxz = max(maxz, z[i][j])
        newx = []
        newy = []
        newz = []
        newx.append(x[0])
        newy.append(y[0])
        newz.append(z[0])
        for i in range(1,len(x)):
            frames = framespmov
            while frames >= 0:
                tx = []
                ty = []
                tz = []
                for j in range(len(x[0])):
                    rfr = framespmov - frames
                    tx.append((x[i-1][j]*frames + x[i][j]*rfr)/framespmov)
                    ty.append((y[i-1][j]*frames + y[i][j]*rfr)/framespmov)
                    tz.append((z[i-1][j]*frames + z[i][j]*rfr)/framespmov)
                frames -= 1
                newx.append(tx)
                newy.append(ty)
                newz.append(tz)
        fig = go.Figure(
            data=[go.Scatter3d(
                x=x[0], y=y[0], z=z[0],
                mode="markers",
                marker=dict(color=colors, size=size),
                showlegend=False)
            ],
            layout=go.Layout(
                title_text=title,
                hovermode="closest",
                scene=dict(
                    xaxis_title="X-Coordinates",
                    yaxis_title="Y-Coordinates",
                    zaxis_title="Z-Coordinates",
                    xaxis=dict(range=[minx-1, maxx+2],autorange=False,zeroline=False),
                    yaxis=dict(range=[miny-1, maxy+2],autorange=False,zeroline=False),
                    zaxis=dict(range=[minz-1, maxz+2],autorange=False,zeroline=False)
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(
                        label="Play",
                        method="animate",
                        args=[None]
                    )]
                )]
            ),
            frames=[go.Frame(
                data=[go.Scatter3d(
                    x=newx[i],
                    y=newy[i],
                    z=newz[i],
                    mode="markers",
                    marker=dict(color=colors, size=size),
                    name='Particles',
                    showlegend=True)
                ],
                layout=go.Layout(
                        scene=dict(
                            xaxis=dict(range=[minx-1, maxx+2], autorange=False,zeroline=False),
                            yaxis=dict(range=[miny-1, maxy+2], autorange=False,zeroline=False),
                            zaxis=dict(range=[minz-1, maxz+2], autorange=False,zeroline=False)
                        )
                    )
                )
                for i in range(0,len(newx))]
        )
        fig.update_scenes(aspectmode="cube")
        return fig
    except Exception as error:
        print(f"An error occurred: {error}")
        return