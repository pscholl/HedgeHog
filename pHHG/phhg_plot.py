class pHhg_plot():
    def __init__(self,user='user0',db='activity-data.sqlite',fig=gcf()):
        # get first data from database
        self.user,self.db,self.n=user,db,int((fig.get_size_inches()*fig.get_dpi())[0]*.7)
        self.d=hhg_sql_dataset(table=user,db=db,n=self.n)

        # poll timer that checks db retrieval
        self.timer=fig.canvas.new_timer(interval=50)
        self.timer.add_callback(self.ontimer)
        self.polling=False

        # do GUI stuff and plot raw accl and env data
        fig.clf()
        self.fig=fig

        self.b_ax=subplot2grid((5,1),(4,0)) # bird's eye view
        self.bird=plot_date(self.d.t,array((self.d.x,self.d.y,self.d.z)).T,'-')
        self.b_ax.grid(color='k', linestyle=':', linewidth=.5)
        setp(self.b_ax.get_yticklabels(),visible=False)
        self.b_ax.set_navigate(False)

        self.a_ax=subplot2grid((5,1),(1,0),rowspan=3)
        self.a_ax.grid(color='k', linestyle=':', linewidth=.5)
        self.a_ax.yaxis.set_label_text('3D Acceleration')
        self.accd=plot_date(self.d.t,array((self.d.x,self.d.y,self.d.z)).T,'-')
        setp(self.a_ax.get_xticklabels(),visible=False)

        self.l_ax=subplot2grid((5,1),(0,0),sharex=self.a_ax)
        self.l_ax.grid(color='k', linestyle=':', linewidth=.5)
        self.l_ax.yaxis.set_label_text('Lightlevel')
        setp(self.l_ax.get_xticklabels(),visible=False)
        self.ligd=plot_date(self.d.t,self.d.l,'-')

        self.t_ax=self.l_ax.twinx()
        self.t_ax.yaxis.set_label_text('Temperature')
        self.temd=plot_date(self.d.t,self.d.temp,'-',color='green')
        setp(self.t_ax.get_xticklabels(),rotation='vertical')

        subplots_adjust(left  = 0.1, right = 0.9, # left, right,
                        bottom = 0.10,top = 0.9, # bottom and top
                        wspace = 0.2,  # width space betw. subplots
                        hspace = 0.1)  # height space btw. subplots

        # care fro proper xtick labels
        for tick in self.l_ax.xaxis.iter_ticks():
            tick[0].label2On = True
            tick[0].label1On = False
            tick[0].label2.set_rotation(20)

        fig.autofmt_xdate(rotation=45)
        fig.canvas.draw()

        # support for bird's eye navigation
        self.xpos   = None
        self.window = None

        # connect callback events
        self.acid=self.a_ax.axes.callbacks.connect('xlim_changed',self.onxlim)
        self.lcid=self.l_ax.axes.callbacks.connect('xlim_changed',self.onxlim)
        self.scid=self.fig.canvas.mpl_connect('scroll_event',self.onscroll)
        self.mcid=self.fig.canvas.mpl_connect('motion_notify_event',self.onmove)
        self.pcid=self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        self.rcid=self.fig.canvas.mpl_connect('button_release_event',self.onrelease)

    def __del__(self):
        # remove callback so we don't leave dangling refs
        self.a_ax.axes.callbacks.disconnect(self.acid)
        self.a_ax.axes.callbacks.disconnect(self.lcid)
        self.fig.canvas.mpl_disconnect(self.scid)
        self.fig.canvas.mpl_disconnect(self.mcid)
        self.fig.canvas.mpl_disconnect(self.pcid)
        self.fig.canvas.mpl_disconnect(self.rcid)

    def onclick(self,event):
        if self.window is not None and self.window.contains(event)[0]:
            self.xpos = event.xdata

    def onrelease(self,event):
        self.xpos = None

    def onmove(self,event):
        if self.xpos is not None and hasattr(event,'data'):
            dt = self.xpos-event.xdata
            self.xpos=event.xdata
            t1,t2=self.a_ax.axes.get_xlim()
            self.a_ax.axes.set_xlim((t1-dt,t2-dt))

    def onscroll(self,event):
        step=sign(event.step)*0.4
        t1,t2=self.a_ax.axes.get_xlim()
        span=((t2-t1)*(1-step)**abs(event.step))/2.
        self.a_ax.axes.set_xlim((event.xdata-span,event.xdata+span))

    def ontimer(self):
        try:
            if self.d.is_alive(): return

            # set new data
            for p,d in zip(flatten((self.accd,self.ligd,self.temd)),\
                    (self.d.x,self.d.y,self.d.z,self.d.l,self.d.temp)):
                p.set_ydata(d)
                p.set_xdata(self.d.t)

            # update plots
            self.polling=False
            self.timer.stop()
            self.fig.canvas.draw()
        except Exception:
            # perhaps need to do some more here (if we ever get here)
            self.polling=False
            self.timer.stop()

    def onxlim(self,event):
        t1,t2=self.a_ax.axes.get_xlim()
        SEC2_55=2.9513845220208168e-05

        self.d.stop() # retrieve new data
        self.d=hhg_sql_dataset(t1=t1-SEC2_55,t2=t2+SEC2_55,
                user=self.user,db=self.db,n=self.n)

        if not self.polling:
            self.polling=True
            self.timer.start()

        if self.window is not None:
            self.window.remove()

        x1=max([max(o.get_ydata()) for o in self.bird])
        x2=min([min(o.get_ydata()) for o in self.bird])

        self.window = self.b_ax.fill_between([t1,t2],[x1,x1],[x2,x2],alpha=.5)
        self.fig.canvas.draw()
