# https://stackoverflow.com/questions/48722899/ray-intersection-misses-the-target
from pyglet.gl import *
from pyglet.window import key
import numpy as np

class CustomGroup(pyglet.graphics.Group):
    # https://stackoverflow.com/questions/4127242/opengl-rendering-two-transparent-planes-intersecting-each-other-impossible-or
    def set_state(self):
        # glDepthMask(GL_FALSE)
        pass
    def unset_state(self):
        # glDepthMask(GL_TRUE)
        pass

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sphere = gluNewQuadric() 
        self.vp_valid = False
        self.mouse_pos = (0, 0)
        self.mv_mat = (GLdouble * 16)()
        self.p_mat  = (GLdouble * 16)()
        self.v_rect = (GLint * 4)()
        self.rx = 0.
        self.ry = 0.
        self.rz = 0.
        self.x = 0.
        self.y = 0.
        self.z = -10
        self.ALT = False
        self.batch = pyglet.graphics.Batch()
        # pyglet.clock.schedule(self.update)

        glEnable(GL_DEPTH_TEST)
        # glDisable(GL_DEPTH_TEST)
        # glDepthFunc(GL_NEVER)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45., 1., 0.1, 800.)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

        # depth_func = glGetIntegerv(GL_DEPTH_FUNC, None)
        # glDepthFunc(GL_ALWAYS)
        # glDepthFunc(GL_LESS)
        # glDepthFunc(GL_GREATER)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glDepthMask(GL_FALSE)
        # glBlendEquation(GL_FUNC_ADD)
        # glBlendFuncSeparate(GL_DST_ALPHA, GL_ONE, GL_ZERO, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_CULL_FACE)

        from colorsys import hsv_to_rgb
        glPointSize(10)
        self.batch.add(10,
                        GL_POINTS,
                        None,
                        ('v3f/static', (np.arange(30) // 3) / 10.),
                        ('c3f/static', np.array(list(map(lambda x: hsv_to_rgb(x, 1., 1.), np.arange(10) / 10))).reshape(-1))
                    )

        # glPointSize(5)
        self.small_points_colors = np.array(list(map(lambda x: hsv_to_rgb(x, 1., 1.), np.arange(10) / 10))).reshape(-1)
        self.small_points = self.batch.add(10,
                            GL_POINTS,
                            None,
                            ('v3f/dynamic', -(np.arange(30)[::-1] // 3) / 13. + 0.5),
                            ('c3f/dynamic', self.small_points_colors)
                        )
        # glDepthMask(GL_FALSE)
        vertices = np.array([[0., 0., 0.], 
                            [1., 0., 0.], 
                            [0., 1., 0.], 
                            [0., 0., 1.]])
        indices = np.array([0, 2, 1, 3, 0, 2])
        self.batch.add_indexed(len(vertices),
                                GL_TRIANGLE_STRIP, # GL_TRIANGLES
                                pyglet.graphics.Group(),
                                # CustomGroup(),
                                indices.reshape(-1),
                                ('v3f/static', vertices.reshape(-1)),
                                ('c4f/static', [0., 0.5, 1., 0.7] * len(vertices)))
        self.batch.add_indexed(len(vertices),
                                GL_TRIANGLE_STRIP,
                                pyglet.graphics.Group(),
                                # CustomGroup(),
                                indices.reshape(-1),
                                ('v3f/static', -vertices.reshape(-1) / 2 + 0.1),
                                ('c4f/static', [0., 1., 0.5, 0.7] * len(vertices)))
        # self.batch.add_indexed(len(vertices),
        #                         GL_TRIANGLE_STRIP,
        #                         CustomGroup(),
        #                         indices.reshape(-1),
        #                         ('v3f/static', -vertices.reshape(-1) / 2 + 0.2),
        #                         ('c4f/static', [1., 0.5, 0., 0.5] * len(vertices)))
        # indices = np.array([[0, 2, 1], 
        #                     [0, 1, 3], 
        #                     [0, 3, 2], 
        #                     [1, 2, 3]])
        # indices = np.row_stack([indices, (indices + 4).astype(int)])
        # self.batch.add_indexed(len(vertices) * 2,
        #                         GL_TRIANGLES,
        #                         pyglet.graphics.Group(),
        #                         indices.reshape(-1),
        #                         ('v3f/static', np.concatenate([vertices.reshape(-1), -vertices.reshape(-1) + 0.3])),
        #                         ('c4f/static', [0., 0.5, 1., 0.7] * len(vertices) + [0., 1., 0.5, 0.7] * len(vertices)))
        # self.batch.add(1,
        #                     GL_POINTS,
        #                     None,
        #                     ('v3f/static', [0, 0, 0]),
        #                     ('c4f/static', [0, 0, 0, 0])
        #                 )

        self.label = pyglet.text.Label('Hello, world',
                          font_name = 'Times New Roman',
                          font_size = 12,
                          x = 10, y = self.height - 10,
                          # x = self.width//2, y = self.height//2,
                          anchor_x = 'left', anchor_y = 'top')
        self.on_resize(self.width, self.height)
        # glDepthMask(GL_TRUE)
        # glDisable(GL_BLEND)
        # glDepthFunc(depth_func)

    def on_resize(self, width, height):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.001, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)

    def isectSphere(self, p0, p1, cpt, radius):

        # normalized ray direction
        r_dir = np.subtract(p0, p1)
        r_dir = r_dir / np.linalg.norm(r_dir)

        # nearest point on the ray to the sphere
        p0_cpt = np.subtract(p0, cpt)
        near_pt = np.subtract(p0, r_dir * np.dot(p0_cpt, r_dir))

        # distance to center point
        dist = np.linalg.norm(np.subtract(near_pt, cpt))

        # intersect if dist less or equal the radius of the sphere 
        return dist <= radius

    # def update(self, dt):
    #     self.rx += dt * 1
    #     self.ry += dt * 80
    #     self.rz += dt * 30
    #     self.rx %= 360
    #     self.ry %= 360
    #     self.rz %= 360

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLoadIdentity()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)

        self.small_points.colors = self.small_points_colors
        if self.ALT:
            glGetDoublev(GL_MODELVIEW_MATRIX, self.mv_mat)
            glGetDoublev(GL_PROJECTION_MATRIX, self.p_mat)
            glGetIntegerv(GL_VIEWPORT, self.v_rect)

            temp_val = [GLdouble() for _ in range(3)]
            gluUnProject(*self.mouse_pos, 0, self.mv_mat, self.p_mat, self.v_rect, *temp_val)
            self.mouse_near = [v.value for v in temp_val]
            gluUnProject(*self.mouse_pos, 1, self.mv_mat, self.p_mat, self.v_rect, *temp_val)
            self.mouse_far = [v.value for v in temp_val]

            small_points_vertices = np.array(self.small_points.vertices).reshape(-1, 3)
            isects = []
            for i in range(len(small_points_vertices)):
                isects.append(
                    self.isectSphere(self.mouse_near, self.mouse_far, 
                    small_points_vertices[i], 0.1)
                )
            for i in np.argwhere(isects):
                self.small_points.colors[int(i * 3):int(i * 3 + 3)] = [1, 0, 0]

        self.batch.draw()

        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();
        gluOrtho2D(0.0, self.width, 0.0, self.height);
        glMatrixMode(GL_MODELVIEW);
        glPushMatrix();
        glLoadIdentity();
        self.label.draw()
        glMatrixMode(GL_MODELVIEW);
        glPopMatrix();
        glMatrixMode(GL_PROJECTION);
        glPopMatrix();
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)


    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)

    # @window.event
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y): # zoom
        with np.errstate(divide = 'ignore', over = 'ignore'):
            self.z += scroll_y * 5 * (1 + 1 / (1 + np.exp((self.z + 5) * 5)**(-1)))

    # @window.event
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.mouse_pos = (x, y)
        key = pyglet.window.key
        if button == pyglet.window.mouse.LEFT and (modifiers & key.MOD_CTRL):
            x -= window.width // 2
            y -= window.height // 2
            lx = x - dx
            ly = y - dy
            angle = np.angle((x + y * 1J) / ((lx + ly * 1J))) * 50
            self.rz += angle
            return
        if button == pyglet.window.mouse.MIDDLE:
            self.x += dx / 10.0
            self.y += dy / 10.0
            return
        if button == pyglet.window.mouse.LEFT:
            self.ry += dx / 5.0
            self.rx -= dy / 5.0
            return
    def on_key_press(self, symbol, modifiers):
        key = pyglet.window.key
        # if  button == pyglet.window.mouse.LEFT and (modifiers & key.MOD_ALT):
        if  symbol == key.ESCAPE:
            exit()
            # return pyglet.event.EVENT_HANDLED
        if  symbol == key.LALT or symbol == key.RALT:
            self.ALT = True
            return
    def on_key_release(self, symbol, modifiers):
        key = pyglet.window.key
        # if  button == pyglet.window.mouse.LEFT and (modifiers & key.MOD_ALT):
        if  symbol == key.LALT or symbol == key.RALT:
            self.ALT = False
            return

if __name__ == "__main__":
    window = Window(width=800, height=600, resizable=True)
    pyglet.app.run()
