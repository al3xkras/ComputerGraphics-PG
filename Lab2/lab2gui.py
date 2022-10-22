import tkinter as tk
from tkinter import *


class ManipulatorGUI:
    def __init__(self, window, manipulator, params=None):
        if params is None:
            params = {"scale_max": 2.5, }
        self.scale_max = params["scale_max"]
        assert self.scale_max > 1
        self.window = window
        self.manipulator = manipulator
        self.scale0 = DoubleVar()
        self.scale1 = DoubleVar()
        self.scale2 = DoubleVar()
        self.rotate0 = IntVar()
        self.rotate1 = IntVar()
        self.rotate2 = IntVar()
        self.rotate3 = IntVar()
        self.lim1min = IntVar()
        self.lim1max = IntVar()
        self.lim2min = IntVar()
        self.lim2max = IntVar()
        self.lim3min = IntVar()
        self.lim3max = IntVar()
        self.lim4min = IntVar()
        self.lim4max = IntVar()
        self._initVars()
        self._drawGUI()

    def _drawGUI(self):
        Spinbox(self.window, textvariable=self.rotate0, width=5, from_=-180, to=180).place(x=20, y=40)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim1min, width=10).place(x=100, y=40)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim1max, width=10).place(x=170, y=40)
        s1 = Scale(self.window, from_=1, to=self.scale_max, orient=tk.HORIZONTAL, length=200, tickinterval=180,
                   resolution=0.01, variable=self.scale0)
        s1.place(x=240, y=20)

        Spinbox(self.window, textvariable=self.rotate1, width=5, from_=-180, to=180).place(x=20, y=100)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim2min, width=10).place(x=100, y=100)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim2max, width=10).place(x=170, y=100)
        s2 = Scale(self.window, from_=1.0, to=self.scale_max, orient=tk.HORIZONTAL, length=200, tickinterval=180,
                   resolution=0.01, variable=self.scale1)
        s2.place(x=240, y=80)

        sb3 = Spinbox(self.window, textvariable=self.rotate2, width=5, from_=-180, to=180)
        sb3.place(x=20, y=160)

        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim3min, width=10).place(x=100, y=160)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim3max, width=10).place(x=170, y=160)
        s3 = Scale(self.window, from_=1.0, to=self.scale_max, orient=tk.HORIZONTAL, length=200, tickinterval=180,
                   resolution=0.01, variable=self.scale2)
        s3.place(x=240, y=140)

        sb4 = Spinbox(self.window, textvariable=self.rotate3, width=5, from_=-180, to=180)
        sb4.place(x=20, y=220)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim4min, width=10).place(x=100, y=220)
        Entry(self.window, bg="#FFFFFF", fg="#000000", textvariable=self.lim4max, width=10).place(x=170, y=220)

    def _initVars(self):
        self.rotate0.set(0)
        self.rotate1.set(0)
        self.rotate2.set(0)
        self.rotate3.set(0)
        self.lim1min.set(-180)
        self.lim1max.set(180)
        self.lim2min.set(-180)
        self.lim2max.set(180)
        self.lim3min.set(-180)
        self.lim3max.set(180)
        self.lim4min.set(-180)
        self.lim4max.set(180)

    def update(self):
        manipulator = self.manipulator
        try:
            if self.rotate0.get() != 0 and abs(self.rotate0.get()) <= 90:
                manipulator.rotate(0, self.rotate0.get())
        except TclError:
            pass
        try:
            if self.rotate1.get() != 0 and abs(self.rotate1.get()) <= 90:
                manipulator.rotate(1, self.rotate1.get())
        except TclError:
            pass
        try:
            if self.rotate2.get() != 0 and abs(self.rotate2.get()) <= 90:
                manipulator.rotate(2, self.rotate2.get())
        except TclError:
            pass
        try:
            if self.rotate3.get() != 0 and abs(self.rotate3.get()) <= 90:
                manipulator.rotate(3, self.rotate3.get())
        except TclError:
            pass

        try:
            if self.scale0.get() != 1:
                manipulator.scale(0, self.scale0.get())
        except TclError:
            pass
        try:
            if self.scale1.get() != 1:
                manipulator.scale(1, self.scale1.get())
        except TclError:
            pass
        try:
            if self.scale2.get() != 1:
                manipulator.scale(2, self.scale2.get())
        except TclError:
            pass

        try:
            angle_lims = [
                (self.lim1min.get(), self.lim1max.get()),
                (self.lim2min.get(), self.lim2max.get()),
                (self.lim3min.get(), self.lim3max.get()),
                (self.lim4min.get(), self.lim4max.get()),
            ]
            for lim in angle_lims:
                assert lim[0] <= 0 and lim[1] >= 0

            manipulator.angle_limits = angle_lims
        except TclError or AssertionError:
            pass
