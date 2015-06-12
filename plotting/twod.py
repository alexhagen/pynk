#import modules
from scipy.optimize import curve_fit
from scipy.odr import *
from math import exp
#set svg as export
import matplotlib
import string
import os
from matplotlib.patches import Ellipse,Polygon
matplotlib.use('pgf')
pgf_with_pdflatex = {
    "font.family": "serif",
    "font.serif": [],
    "axes.linewidth": 0.5,
    "axes.edgecolor": "#746C66",
    "xtick.major.width" : 0.25,
    "xtick.major.size" : 2,
    "xtick.direction" : "in",
    "xtick.minor.width" : 0.125,
    "xtick.color": "#746C66",
    "ytick.major.width" : 0.25,
    "ytick.major.size" : 2,
    "ytick.minor.width" : 0.125,
    "ytick.color": "#746C66",
    "ytick.direction" : "in",
    "text.color": "#746C66",
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "axes.labelcolor": "#746C66",
    "xtick.labelsize": "x-small",
    "ytick.labelsize": "x-small",
    "axes.labelsize": "medium",
    "legend.fontsize": "x-small",
    "legend.frameon": False,
    "axes.grid"     : False,
    "grid.color"    : "#A7A9AC",   # grid color
    "grid.linestyle": ":",       # dotted
    "grid.linewidth": 0.125,     # in points
    "grid.alpha"    : 0.5,     # transparency, between 0.0 and 1.0
    "savefig.transparent" : True,
    "path.simplify" : True
}
'''
    "path.simplify" : True,
    "axes.formatter.use_mathtext" : True,
    "axes.below" : True
'''
matplotlib.rcParams.update(pgf_with_pdflatex)
import matplotlib.pyplot as plt
plt.close("all")
import numpy as np
#from mpl_toolkits.axes_grid.axislines import Subplot
#import matplotlib.animation as animation

#make the line graphing class
class ah2d(object):
    leg=False;
    leg_col_one_col = 2
    leg_col_two_col = 3
    leg_col_full_page = 4
    marker = {0: '+',
              1: '.',
              2: '1',
              3: '1',
              4: '2',
              5: '3',
              6: '4'}
    linestyle = {0: '-',
            1: '--',
            2: '-.',
            3: ':'};
    sizestring = {'1': 'onecolumn',
            '2': 'twocolumn',
            'fp': 'fullpage',
            'cs': 'customsize',
            'none': ''};
    def __init__(self):
        self.fig = plt.figure();
        self.ax = self.fig.add_subplot(111);
        self.ax_subp = [];
        self.ax2 = None;
        self.ax.spines['top'].set_visible(False);
        self.ax.spines['right'].set_visible(False);
        self.ax.get_xaxis().tick_bottom();
        self.ax.get_yaxis().tick_left();
        self.artists = [];
        self.landscape = True;
        self.width = 3.25;
        self.height = self.width/1.61803398875;
        self.plotnum = 0;
        self.regnum = 0;
        self.lines = {};
        self.bars = {};
        self.regs = {};
        self.reg_string = {};
    def xlabel(self,label,axes=None):
        if axes is None:
            axes = self.ax;
        xlab=axes.set_xlabel(label);
        self.artists.append(xlab);
    def add_subplot(self,subp=121):
        gsstr = str(subp);
        gs1 = int(gsstr[0]);
        gs2 = int(gsstr[1]);
        self.ax.change_geometry(gs1,gs2,1);
        self.ax2.change_geometry(gs1,gs2,1);
        self.ax_subp.append(self.fig.add_subplot(subp));
    def title(self,title):
        ttl=self.ax.set_title(title);
        self.artists.append(ttl);
    def ylabel(self,label,axes=None):
        if axes is None:
            axes = self.ax;
        ylab=axes.set_ylabel(label);
        self.artists.append(ylab);
    def xlim(self,minx,maxx,axes=None):
        self.ax.set_xlim([minx,maxx]);
    def ylim(self,miny,maxy,axes=None):
        self.ax.set_ylim([miny,maxy]);
    def legend(self):
        self.ax.legend();
        (legobjs,legtitles) = self.ax.get_legend_handles_labels();
        inc_objs = [];
        inc_titles = [];
        for i in range(0,len(legtitles)):
            if 'connector' not in legtitles[i]:
                inc_objs.append(legobjs[i]);
                inc_titles.append(legtitles[i]);
        self.ax.legend(inc_objs,inc_titles);
    def xticks(self,ticks,labels,axes=None):
        if axes is not None:
            plt.sca(axes);
        else:
            plt.sca(self.ax);
        plt.xticks(ticks,labels);
    def yticks(self,ticks,labels,axes=None):
        if axes is not None:
            plt.sca(axes);
        else:
            plt.sca(self.ax);
        plt.yticks(ticks,labels);
    def markers_on(self):
        for key in self.lines:
            self.lines[key].set_alpha(1.0)
            self.lines[key].set_markersize(6)
    def markers_off(self):
        for key in self.lines:
            self.lines[key].set_markersize(0)
    def lines_on(self):
        for key in self.lines:
            self.lines[key].set_linewidth(1.0)
    def lines_off(self):
        for key in self.lines:
            self.lines[key].set_linewidth(0.0)
    def add_vline(self,x,ymin,ymax,ls='solid',lw=0.5):
        return plt.vlines(x,ymin,ymax,linestyles=ls,linewidths=lw);
    def add_hline(self,y,xmin=None,xmax=None,ls='solid',lw=1.5,color='red'):
        return plt.axhline(y,linestyle=ls,linewidth=lw,color=color);
    def add_label(self,x,y,string):
        curve_place = (x,y);
        self.ax.annotate(string, 
                        xy=curve_place, 
                        xytext=curve_place);
    def add_data_pointer(self,x,curve=None,point=None,string=None,
                         place='up-right',axes=None):
        if axes is None:
            axes = self.ax;
        
        if curve is not None:
            y = curve.at(x);
        elif point is not None:
            y = point;
        else:
            raise Exception('No point for the arrow given in reference to ' + \
                'data pointer.');
        if string is None:
            string = '$\left( %f,%f \\right)$' % (x,y);
        if place == 'up-right':
            curve_place = (4.0*x/3.0,4.0*y/3.0);
        elif place == 'up-left':
            curve_place = (3.0*x/4.0,4.0*y/3.0);
        elif place == 'down-right':
            curve_place = (4.0*x/3.0,3.0*y/4.0);
        elif place == 'down-left':
            curve_place = (2.0*x/4.0,3.0*y/4.0);
        elif type(place) is tuple:
            curve_place = place;
        axes.annotate(string, 
                        xy=(x,y), 
                        xytext=curve_place,
                        arrowprops=dict(arrowstyle="fancy",
                                        fc="0.3",ec="none",
                                        patchB = Ellipse((2, -1), 0.5, 0.5),
                                        connectionstyle = \
                                            "angle3,angleA=0,angleB=-90")
                        )
    def add_reg_line(self,x,y,regtype='lin',name='reg',xerr=None,yerr=None):
        self.regnum = self.regnum+1;
        if name is 'reg':
            name = 'reg%d' % (self.regnum);
        # set up the error bounds
        if yerr is None:
            y_err_up = None;
            y_err_down = None;
        # determine the regression
        if regtype.isdigit():
            # determine the coefficients of degree regtype
            coeffs = np.polyfit(x,y,regtype);
            # determine a fine grid of values
            x_fit = np.linspace(min(x),max(x),num=1000);
            y_fit = np.polyval(coeffs,x_fit);
            self.coeffs = coeffs;
            name = '$y\left( x \\right) = ';
            for i in range(0,int(regtype)):
                if coeffs[i] > 0:
                    name += '+ %f' % (abs(coeffs[i]));
                    if i > 0:
                        name += 'x^{%d}' % (i);
                elif coeffs[i] < 0:
                    name += '- %f' % (abs(coeffs[i]));
                    if i > 0:
                        name += 'x^{%d}' % (i);
            name += '$';
            print name;
        elif regtype is 'exp':
            x_np = np.array(x);
            x_err_np = np.array(xerr);
            y_np = np.array(y);
            y_err_np = np.array(yerr);
            #coeffs = np.polyfit(x,y_log,1);
            #x_fit = np.linspace(min(x),max(x),num=1000);
            #y_fit_log = np.polyval(coeffs,x_fit);
            #y_fit = np.exp(y_fit_log);
            def exp_func(B,x):
                return B[0]*np.exp(B[1]*x);
            
            exp_model = Model(exp_func);
            exp_data = RealData(x_np,y_np,sx=x_err_np,sy=y_err_np);
            odr = ODR(exp_data,exp_model,beta0=[0.,1.])
            out = odr.run();
            if out.res_var > 1.0 and out.beta[1] < 0.0:
                x_fit = np.linspace(min(x),max(x),num=1000);
                y_fit = exp_func(out.beta,x_fit);
                self.reg_string[name] = '$t_{wait} = e^{%.2f \cdot p} + %.2f$' % (out.beta[1],out.beta[0]);
                if out.sum_square < 20:
                    y_err_up = exp_func(out.beta+out.sd_beta,x_fit);
                    y_err_down = exp_func(out.beta-out.sd_beta,x_fit);
                    if y_err_up[0] > 120:
                        y_err_up = None;
                        y_err_down = None;
                else:
                    y_err_up = None;
                    y_err_down = None;
                    print "showing the exponential error will occlude data";
            else:
                y_fit = None;
                x_fit = None;
                y_err_up = None;
                y_err_down = None;
                print "the exponential does not fit to the data";
        elif regtype is 'log':
            print 'I haven\'t yet completed the log fitting!';            
            #do something;
        elif regtype is 'gaussian':
            def gaus(x,a,x0,sigma):
                return a*exp(-(x-x0)**2/(2*sigma**2));
            pop,pcov = curve_fit(gaus,x,y,p0=[1,np.mean(y),np.std(y)]);
            x_fit = x_fit = np.linspace(min(x),max(x),num=1000);
            y_fit = gaus(x_fit);
        # plot the regression
        if x_fit is not None and y_fit is not None:
            self.x_fit = x_fit;
            self.y_fit = y_fit;
            lines = plt.plot(x_fit,y_fit,label=name,color='#A7A9AC',ls='--');
            self.regs[name] = lines[0];
            # make sure these are lines
            lines[0].set_markersize(0);
            lines[0].set_lw(1.0);
        if y_err_up is not None and y_err_down is not None:
            uperrlines = plt.plot(x_fit,y_err_up,color='#D1D3D4',ls='--');
            downerrlines = plt.plot(x_fit,y_err_down,color='#D1D3D4',ls='--');
            self.ax.fill_between(x_fit,y_err_up,y_err_down,facecolor='#D1D3D4',alpha=0.5,lw=0.0);
            # add the regression to the dict of regressions
    def add_wt_info_box(self,ctmfd_data):        
        textstr = "ctmfd: $%s$\n" % (ctmfd_data.ctmfd);
        textstr += "fluid: %s\n" % (ctmfd_data.fluid);
        textstr += "source: %s at $%s\,\mathrm{cm}$\n" % (ctmfd_data.source,
                        str(ctmfd_data.source_dist_cm).strip('[]'));
        textstr += "temperature: $%.1f\,\mathrm{\,^{o}C}$\n" % (ctmfd_data.temperature);
        textstr += "performed on: %d/%d/%d\n" % (ctmfd_data.month,ctmfd_data.day,ctmfd_data.year);
        print self.reg_string
        if self.reg_string is not {}:
            for key in self.reg_string:
                textstr += "reg: %s\n" % (self.reg_string[key]);
        posx = 1 - (0.05/1.61803398875);
        posy = 1 - (0.05);
        self.ax.text(posx, posy, textstr, transform=self.ax.transAxes,
                     fontsize='xx-small',va='top',ha='right')
    def fill_between(self,x,y1,y2,fc='red',name='plot',axes=None):
        if axes is None:
            axes = self.ax;
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum);
        axes.fill_between(x,y1,y2,facecolor=fc,alpha=0.5);
        patch = axes.add_patch(Polygon([[0,0],[0,0],[0,0]],facecolor=fc,alpha=0.5,label=name));
        self.bars[name]=patch;
    def add_line(self,x,y,name='plot',xerr=None,yerr=None,linewidth=0.5,linestyle=None,legend=True):
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        if linestyle is None:
            _ls = self.linestyle[self.plotnum%4];
        else:
            _ls = linestyle;
        if xerr is None and yerr is None:
            line=plt.plot(x,y,label=name,color='black',
                marker=self.marker[self.plotnum%7],
                ls=_ls,lw=linewidth,solid_capstyle='butt');
            for i in range(0,len(line)):
                self.lines[name+'%d' % (i)] = (line[i])
        else:
            line,caplines,barlinecols=plt.errorbar(x,y,label=name,color='black',
                xerr=xerr,yerr=yerr,marker=self.marker[self.plotnum%7],
                ls=_ls,ecolor='#A7A9AC',lw=linewidth);
            self.lines[name] = (line)
        self.markers_on();
        self.lines_off();
    def add_line_yy(self,x,y,name='plot',xerr=None,yerr=None,linewidth=0.5,linestyle=None,legend=True):
        # make new axis
        self.ax2 = self.ax.twinx()
        self.add_line(x,y,name=name,xerr=xerr,yerr=yerr,linewidth=linewidth,linestyle=linestyle,legend=legend);
    def add_xx(self,calfunc):
        self.ax2 = self.ax.twiny();
        mini = calfunc(np.min(self.ax.get_xlim()));
        maxi = calfunc(np.max(self.ax.get_xlim()));
        self.ax2.set_xlim(mini,maxi);
        self.ax2.get_xaxis().tick_top();
    def add_hist(self,y,bins,name='plot'):
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        n,bins,patches=plt.hist(y,bins=bins,label=name,facecolor='gray',alpha=0.5,normed=False);
        self.bars[name] = patches;
        return n,bins;
    def add_bar(self,x,y,name='plot'):
        self.plotnum=self.plotnum+1;
        if name is 'plot':
            name = 'plot%d' % (self.plotnum)
        delta = [j-i for i, j in zip(x[:-1], x[1:])];
        delta.append(delta[-1]);
        #x = [j - (i/2) for i, j in zip(delta, x)];
        patches=plt.bar(x,y,width=delta,label=name,facecolor='gray',alpha=0.5);
        self.bars[name] = patches;
        return x,y,delta;
    def add_waiting_time(self,ctmfd_data,name='plot'):
        p = [];
        perr = [];
        wt = [];
        wterr = [];
        for key in ctmfd_data.data_split:
            p.append(ctmfd_data.data_split[key].p);
            perr.append(2*ctmfd_data.data_split[key].p_sigma);
            wt.append(ctmfd_data.data_split[key].wt);
            wterr.append(2*ctmfd_data.data_split[key].wt_sigma);
        self.add_line(p,wt,xerr=perr,yerr=wterr,name=name)
    def add_legend(self):
        self.leg=True
        leg = self.ax.legend();
        self.artists.append(leg);
    def det_height(self):
        if self.landscape:
            self.height = self.width/1.61803398875;
        else:
            self.height = self.width*1.61803398875;
    def remove_font_sizes(self,filename):
        f=open(filename,'r')
        fstring = "\\centering \n" + f.read()
        f.close()
        f=open(filename,'w')
        fstring=fstring.replace("\\rmfamily\\fontsize{8.328000}{9.993600}\\selectfont","\\scriptsize")
        fstring=fstring.replace("\\rmfamily\\fontsize{12.000000}{14.400000}\\selectfont","\\normalsize")       
        fstring = filter(lambda x: x in string.printable, fstring);
        f.write(fstring)
        f.close()
    def long_name(self):
        self.leg_col_one_col = 1
        self.leg_col_two_col = 1
        self.leg_col_full_page = 1
    def set_size(self,size,sizeofsizes,customsize=None):
        if size is '1':
            self.width=3.25;
            self.det_height();
            if self.leg:        
                self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                    ncol=self.leg_col_one_col, mode="expand", 
                    borderaxespad=0.);
        elif size is '2':
            self.width=6.25;
            self.det_height();
            self.height = self.height/2.0;
            self.fig.set_size_inches(self.width,self.height);
            if self.leg:        
                self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                               ncol=self.leg_col_two_col, mode="expand", 
                               borderaxespad=0.);
        elif size is 'fp':
            elf.width=10;
            self.det_height();
            self.fig.set_size_inches(self.width,self.height);
            if self.leg:        
                self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                               ncol=self.leg_col_full_page, mode="expand", 
                               borderaxespad=0.);
        elif size is 'cs':
            if customsize is not None:
                self.width=customsize[0];
                self.height=customsize[1];
        self.fig.set_size_inches(self.width,self.height);
    def export_fmt(self,filename,size,sizeofsizes,format):
        if sizeofsizes == 1:
            size = 'none';
        if format is 'png':
            add = '.png';
        elif format is 'pgf':
            add = '.pgf';
        elif format is 'svg':
            # save as pdf, then pdf2svg
            plt.savefig(filename+self.sizestring[size]+'.pdf',
                bbox_extra_artists=self.artists,bbox_inches='tight');
            os.system('pdf2svg '+filename+self.sizestring[size]+'.pdf '+
                filename+self.sizestring[size]+'.svg');
            os.remove(filename+self.sizestring[size]+'.pdf');
        elif format is 'websvg':
            add = 'web.svg';
        if format is not 'svg':
            plt.savefig(filename+self.sizestring[size]+add,
                bbox_extra_artists=self.artists,bbox_inches='tight');
        if format is 'pgf':
            self.remove_font_sizes(filename+self.sizestring[size]+add);
    def export(self,filename,sizes=['1'],formats=['pgf'],customsize=None):
        for size in sizes:
            for format in formats:
                self.set_size(size,len(sizes),customsize=customsize);
                self.export_fmt(filename,size,len(sizes),format);
