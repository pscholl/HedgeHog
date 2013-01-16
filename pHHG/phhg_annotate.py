class AnnotateTool():
    """ shift-click event handler for handling annotations, will register on the first
    call and de-register on second call.

    doc http://matplotlib.sourceforge.net/users/event_handling.html
    """
    def __init__(self,annotations=[],activities=None,
            canvas=gcf().canvas,pickeraxes=None,displayaxes=None):
        """ supply the current list of activities as rec.array
        (with t1,t2,name where t1,t2 are starttimes and name is the activity's
        name). The canvas to add the toolbar to and the axes to draw the
        annotations on.

        Add an event handler for shift-clicks to create annotations.
        """
        self.cid=None
        self.canvas=canvas
        self.annotations=annotations

        if pickeraxes is None: pickeraxes=gca()
        if displayaxes is None: displayaxes=gca()

        self.pickeraxes=[pickeraxes] if not iterable(pickeraxes) else pickeraxes
        displayaxes=[displayaxes] if not iterable(displayaxes) else displayaxes
        self.axes=self.pickeraxes+displayaxes

        if activities is not None:
            self.activities=activities
        elif annotations is not []:
            self.activities=set(annotations.activity)
        else:
            raise Exception("needs annotation array or possible activities")

        self.plot_annotations()
        self.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self,event):
        if event.button==1 and event.inaxes in self.pickeraxes:
            b=[b for b in self.blocks if b.contains(event)[0]]
            if len(b)>=1:
                t1,t2=amin(b[0].get_paths()[0].vertices[:-1],axis=0)[0],\
                      amax(b[0].get_paths()[0].vertices[:-1],axis=0)[0]
                self.axes[0].set_xlim((t1,t2))

    def plot_annotations(self):
        self.blocks=[]

        for ax in [ax for ax in self.axes if ax.has_data()]:
            y1,y2=nanmin([o.get_ydata() for o in ax.get_lines()]),\
                  nanmax([o.get_ydata() for o in ax.get_lines()])
            for t1,t2 in zip(self.annotations.t1,self.annotations.t2):
                b=ax.fill_between([t1,t2],[y1,y1],[y2,y2],alpha=.5,color='yellow')
                self.blocks.append(b)

        self.canvas.draw()
