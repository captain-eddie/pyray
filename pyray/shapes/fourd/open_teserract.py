import numpy as np
import queue
from collections import defaultdict
from itertools import combinations
from pyray.shapes.solid.open_cube import char2coord, Face, GraphCube
from pyray.rotation import general_rotation, rotate_points_about_axis,\
    rotation
from pyray.misc import zigzag3
import pyray.shapes.fourd.tesseract_graph as tg
from PIL import Image, ImageDraw


def tst():
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r = rotation(4, np.pi/6)
    f = tg.Face1('00++')
    f.plot(draw, r, scale=40,
           shift=np.array([256, 256, 0, 0]),
           rgba=(125, 125, 12, 80),
           wdh=1)
    im.save("Images//RotatingCube//im" + str(0).rjust(4, '0') + ".png")


def tst2():
    for ix in range(60):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = tg.Face1(''.join(fc))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
        im.save("Images//RotatingCube//im" + str(ix).rjust(4, '0') + ".png")


def tst3():
    ix = 18
    for ii in np.arange(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        theta = np.pi/2*ii/10.0
        # Generate all faces.
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = tg.Face1(''.join(fc))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
        f = tg.Face1('0+0+')
        f.simple_rotate(theta, [0, 3])
        f.plot(draw, r, scale=40,
               shift=np.array([256, 256, 0, 0]),
               rgba=(120, 90, 120, 90),
               wdh=1)
        im.save("Images//RotatingCube//im" + str(ii).rjust(4, '0') + ".png")


def tst4():
    ix = 18
    for ii in np.arange(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        theta = -np.pi/2*ii/10.0
        # Generate all faces.
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = tg.Face1(''.join(fc))
                    if f.val[1] == '+':
                        f.shift_and_simpl_rotate(theta, [1, 3], np.array([0,1,0,1]))
                    elif f.val[1] == '-':
                        f.shift_and_simpl_rotate(-theta, [1, 3], np.array([0,-1,0,1]))
                    elif f.val[2] == '+':
                        f.shift_and_simpl_rotate(theta, [2, 3], np.array([0,0,1,1]))
                    elif f.val[2] == '-':
                        f.shift_and_simpl_rotate(-theta, [2, 3], np.array([0,0,-1,1]))
                    elif f.val[0] == '+':
                        f.shift_and_simpl_rotate(theta, [0, 3], np.array([1,0,0,1]))
                    elif f.val[0] == '-':
                        f.shift_and_simpl_rotate(-theta, [0, 3], np.array([-1,0,0,1]))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
                    if f.val[3] == '+':
                        f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(180, 190, 70, 50),
                           wdh=1)
        im.save("Images//RotatingCube//im" + str(ii).rjust(4, '0') + ".png")


def to_plot1(tf, strt_key='00++'):
    tf.to_plot = {strt_key}
    for k in tf.adj[strt_key].keys():
        tf.to_plot.add(k)
    #for k in tf.face_map.keys():
    #    if k[3] == '+':
    #        tf.to_plot.add(k)


def to_plot2(tf, strt_key='00++'):
    tf.to_plot = {strt_key}
    k = strt_key
    visited = {k}
    for i in range(2):
        for kk in tf.adj[k].keys():
            if kk not in visited:
                tf.to_plot.add(kk)
                visited.add(kk)
                print("Second face: " + kk)
                k = kk
                break


def tst_open_tsrct():
    tf = tg.TsrctFcGraph(angle=np.pi/2)
    tf.r = rotation(4, np.pi*17/60.0)
    return plot_open(tf)


def plot_open(tf, strt_key='00++', to_plot=to_plot2):
    tf.reset_rotations()
    print(len(tf.adj[strt_key].keys()))
    if False:
        to_plot(tf)
    for i in range(2):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf.draw = draw
        tf.reset_vert_col()
        tf.dfs_plot(strt_key)
        tf.reset_vert_col()
        tf.dfs_flatten(strt_key)
        im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")
    return tf


def tst_specific_faces():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00++')
    f2 = tg.Face1('0-+0')
    f3 = tg.Face1('+0+0')
    rot1 = tg.get_rot(f1, f2)
    rot2 = tg.get_rot(f2, f3)
    for i in range(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        
        f1.plot(draw, r)
        f2.plot(draw, r)
        f3.plot(draw, r)

        f3.shift_and_simpl_rotate(np.pi/2*1/10.0, *rot1)
        #f3.shift_and_simpl_rotate(np.pi/2*1/10.0, *rot1)
        f2.shift_and_simpl_rotate(np.pi/2*1/10.0, *rot1)
        
        im.save("Images//RotatingCube//im" +
                    str(i).rjust(4, '0') + ".png")
    for i in range(12):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        
        f1.plot(draw, r)
        f2.plot(draw, r)
        f3.plot(draw, r)
        
        f3.shift_and_simpl_rotate(np.pi/2*1/10.0, *rot2)

        im.save("Images//RotatingCube//im" +
                    str(11+i).rjust(4, '0') + ".png")

