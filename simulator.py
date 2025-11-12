"""
3D Projectile Motion Simulator
Main application module
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Color scheme - dark aesthetic with black, white, gray, blue, and yellow
COLORS = {
    'background': (0.05, 0.05, 0.05),  # Almost black
    'grid': (0.2, 0.2, 0.2),  # Dark gray
    'trajectory': (0.3, 0.6, 1.0),  # Blue
    'object': (0.9, 0.9, 0.9),  # Light gray/white
    'text_bg': (0.1, 0.1, 0.1),  # Dark background for text
    'text': (1.0, 1.0, 1.0),  # White text
    'highlight': (1.0, 0.9, 0.2),  # Yellow
    'axis_x': (0.8, 0.2, 0.2),  # Red for X axis
    'axis_y': (0.2, 0.8, 0.2),  # Green for Y axis
    'axis_z': (0.2, 0.2, 0.8),  # Blue for Z axis
}


class Object3D:
    """Represents a 3D object with physics properties"""
    
    OBJECTS = {
        'football': {'mass': 0.43, 'size': 0.11, 'shape': 'sphere', 'name': 'Football'},
        'basketball': {'mass': 0.62, 'size': 0.12, 'shape': 'sphere', 'name': 'Basketball'},
        'baseball': {'mass': 0.145, 'size': 0.037, 'shape': 'sphere', 'name': 'Baseball'},
        'cube_small': {'mass': 1.0, 'size': 0.1, 'shape': 'cube', 'name': 'Small Cube'},
        'cube_large': {'mass': 5.0, 'size': 0.2, 'shape': 'cube', 'name': 'Large Cube'},
        'spear': {'mass': 0.8, 'size': 0.3, 'shape': 'cylinder', 'name': 'Spear'},
        'arrow': {'mass': 0.02, 'size': 0.15, 'shape': 'cylinder', 'name': 'Arrow'},
        'bullet': {'mass': 0.008, 'size': 0.02, 'shape': 'sphere', 'name': 'Bullet'},
    }
    
    def __init__(self, object_type):
        if object_type not in self.OBJECTS:
            object_type = 'football'
        
        obj_data = self.OBJECTS[object_type]
        self.mass = obj_data['mass']
        self.size = obj_data['size']
        self.shape = obj_data['shape']
        self.name = obj_data['name']
        self.type = object_type
        
        # Physics state
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.angular_velocity = np.array([0.0, 0.0, 0.0])
        
        # Trajectory tracking
        self.trajectory = []
        
    def reset(self, position):
        """Reset object to initial position"""
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.angular_velocity = np.array([0.0, 0.0, 0.0])
        self.trajectory = [self.position.copy()]
        
    def apply_force(self, force_magnitude, angle_horizontal, angle_vertical):
        """Apply force to object at specified angles"""
        # Convert angles from degrees to radians
        h_rad = math.radians(angle_horizontal)
        v_rad = math.radians(angle_vertical)
        
        # Calculate velocity components
        vx = force_magnitude * math.cos(v_rad) * math.cos(h_rad) / self.mass
        vy = force_magnitude * math.sin(v_rad) / self.mass
        vz = force_magnitude * math.cos(v_rad) * math.sin(h_rad) / self.mass
        
        self.velocity = np.array([vx, vy, vz])
        
    def update(self, dt, gravity=-9.81):
        """Update physics simulation"""
        # Apply gravity
        self.velocity[1] += gravity * dt
        
        # Update position
        self.position += self.velocity * dt
        
        # Update rotation
        self.rotation += self.angular_velocity * dt
        
        # Store trajectory point
        if len(self.trajectory) == 0 or np.linalg.norm(self.position - self.trajectory[-1]) > 0.1:
            self.trajectory.append(self.position.copy())
        
        # Check if object hit ground
        if self.position[1] < 0:
            return False
        return True
        
    def draw(self):
        """Draw the 3D object"""
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        glColor3f(*COLORS['object'])
        
        if self.shape == 'sphere':
            quadric = gluNewQuadric()
            gluSphere(quadric, self.size, 20, 20)
            gluDeleteQuadric(quadric)
        elif self.shape == 'cube':
            self._draw_cube(self.size)
        elif self.shape == 'cylinder':
            quadric = gluNewQuadric()
            glRotatef(90, 0, 1, 0)
            gluCylinder(quadric, self.size * 0.3, self.size * 0.3, self.size * 2, 10, 10)
            gluDeleteQuadric(quadric)
            
        glPopMatrix()
        
    def _draw_cube(self, size):
        """Draw a cube"""
        vertices = [
            [-size, -size, -size], [size, -size, -size], [size, size, -size], [-size, size, -size],
            [-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3fv(vertices[0]); glVertex3fv(vertices[1]); glVertex3fv(vertices[2]); glVertex3fv(vertices[3])
        # Back face
        glVertex3fv(vertices[4]); glVertex3fv(vertices[5]); glVertex3fv(vertices[6]); glVertex3fv(vertices[7])
        # Top face
        glVertex3fv(vertices[3]); glVertex3fv(vertices[2]); glVertex3fv(vertices[6]); glVertex3fv(vertices[7])
        # Bottom face
        glVertex3fv(vertices[0]); glVertex3fv(vertices[1]); glVertex3fv(vertices[5]); glVertex3fv(vertices[4])
        # Right face
        glVertex3fv(vertices[1]); glVertex3fv(vertices[2]); glVertex3fv(vertices[6]); glVertex3fv(vertices[5])
        # Left face
        glVertex3fv(vertices[0]); glVertex3fv(vertices[3]); glVertex3fv(vertices[7]); glVertex3fv(vertices[4])
        glEnd()
        
    def draw_trajectory(self):
        """Draw the trajectory path"""
        if len(self.trajectory) < 2:
            return
            
        glColor3f(*COLORS['trajectory'])
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        for point in self.trajectory:
            glVertex3fv(point)
        glEnd()
        glLineWidth(1.0)


class Camera:
    """3D Camera with movement controls"""
    
    def __init__(self):
        self.position = np.array([10.0, 5.0, 10.0])
        self.target = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.yaw = -135.0
        self.pitch = -20.0
        self.distance = 15.0
        
    def update_position(self):
        """Update camera position based on yaw, pitch, and distance"""
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        self.position[0] = self.target[0] + self.distance * math.cos(pitch_rad) * math.cos(yaw_rad)
        self.position[1] = self.target[1] + self.distance * math.sin(pitch_rad)
        self.position[2] = self.target[2] + self.distance * math.cos(pitch_rad) * math.sin(yaw_rad)
        
    def apply(self):
        """Apply camera transformation"""
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )
        
    def rotate(self, dyaw, dpitch):
        """Rotate camera"""
        self.yaw += dyaw
        self.pitch += dpitch
        self.pitch = max(-89, min(89, self.pitch))
        self.update_position()
        
    def zoom(self, delta):
        """Zoom camera in/out"""
        self.distance += delta
        self.distance = max(2, min(50, self.distance))
        self.update_position()
        
    def pan(self, dx, dz):
        """Pan camera target"""
        yaw_rad = math.radians(self.yaw)
        self.target[0] += dx * math.cos(yaw_rad) - dz * math.sin(yaw_rad)
        self.target[2] += dx * math.sin(yaw_rad) + dz * math.cos(yaw_rad)
        self.update_position()


class PhysicsSimulator:
    """Main physics simulator application"""
    
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Projectile Motion Simulator")
        
        # OpenGL setup
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Projection
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Camera
        self.camera = Camera()
        
        # Simulation state
        self.current_object = Object3D('football')
        self.current_object.reset([0, 2, 0])
        self.object_type_index = 0
        self.object_types = list(Object3D.OBJECTS.keys())
        
        self.is_simulating = False
        self.launch_angle_h = 45.0  # Horizontal angle
        self.launch_angle_v = 45.0  # Vertical angle
        self.launch_force = 20.0
        
        # Mouse control
        self.mouse_pressed = False
        self.last_mouse_pos = (0, 0)
        
        # Font for UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # Cursor position in 3D space
        self.cursor_3d_pos = np.array([0.0, 0.0, 0.0])
        
    def draw_grid(self, size=20, spacing=2):
        """Draw ground grid"""
        glColor3f(*COLORS['grid'])
        glBegin(GL_LINES)
        for i in range(-size, size + 1, spacing):
            glVertex3f(i, 0, -size)
            glVertex3f(i, 0, size)
            glVertex3f(-size, 0, i)
            glVertex3f(size, 0, i)
        glEnd()
        
    def draw_axes(self, length=5):
        """Draw coordinate axes"""
        glLineWidth(3.0)
        
        # X axis - Red
        glColor3f(*COLORS['axis_x'])
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        glEnd()
        
        # Y axis - Green
        glColor3f(*COLORS['axis_y'])
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        glEnd()
        
        # Z axis - Blue
        glColor3f(*COLORS['axis_z'])
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        
        glLineWidth(1.0)
        
    def get_cursor_3d_position(self, mouse_pos):
        """Convert 2D mouse position to 3D world coordinates"""
        # Get viewport, modelview, and projection matrices
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        
        # Convert mouse coordinates to OpenGL coordinates
        x = mouse_pos[0]
        y = viewport[3] - mouse_pos[1]
        
        # Read depth at mouse position
        try:
            z = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)[0][0]
            # Unproject to get 3D coordinates
            pos = gluUnProject(x, y, z, modelview, projection, viewport)
            return np.array(pos)
        except:
            return np.array([0.0, 0.0, 0.0])
            
    def draw_ui_text(self, text, x, y, color=(255, 255, 255), font=None):
        """Draw text on screen using pygame surface"""
        if font is None:
            font = self.font
            
        text_surface = font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + text_surface.get_width(), y)
        glTexCoord2f(1, 1); glVertex2f(x + text_surface.get_width(), y + text_surface.get_height())
        glTexCoord2f(0, 1); glVertex2f(x, y + text_surface.get_height())
        glEnd()
        
        glDeleteTextures([texture])
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
    def draw_ui(self):
        """Draw UI overlay with controls and information"""
        # Draw panel background
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        
        # Right panel background
        panel_width = 250
        glColor4f(0.1, 0.1, 0.1, 0.85)
        glBegin(GL_QUADS)
        glVertex2f(self.width - panel_width, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width - panel_width, self.height)
        glEnd()
        
        glEnable(GL_DEPTH_TEST)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        # Draw text information
        y_offset = self.height - 30
        x_offset = self.width - 240
        line_height = 25
        
        # Cursor position
        self.draw_ui_text("Cursor Position:", x_offset, y_offset, (255, 255, 100))
        y_offset -= line_height
        self.draw_ui_text(f"X: {self.cursor_3d_pos[0]:.2f}", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height
        self.draw_ui_text(f"Y: {self.cursor_3d_pos[1]:.2f}", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height
        self.draw_ui_text(f"Z: {self.cursor_3d_pos[2]:.2f}", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height * 1.5
        
        # Object info
        self.draw_ui_text(f"Object: {self.current_object.name}", x_offset, y_offset, (255, 255, 100))
        y_offset -= line_height
        self.draw_ui_text(f"Mass: {self.current_object.mass:.3f} kg", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height * 1.5
        
        # Launch parameters
        self.draw_ui_text("Launch Settings:", x_offset, y_offset, (255, 255, 100))
        y_offset -= line_height
        self.draw_ui_text(f"H-Angle: {self.launch_angle_h:.1f}°", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height
        self.draw_ui_text(f"V-Angle: {self.launch_angle_v:.1f}°", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height
        self.draw_ui_text(f"Force: {self.launch_force:.1f} N", x_offset, y_offset, (255, 255, 255), self.small_font)
        y_offset -= line_height * 1.5
        
        # Status
        status = "SIMULATING" if self.is_simulating else "READY"
        color = (100, 255, 100) if not self.is_simulating else (255, 255, 100)
        self.draw_ui_text(f"Status: {status}", x_offset, y_offset, color)
        y_offset -= line_height * 2
        
        # Controls
        self.draw_ui_text("Controls:", x_offset, y_offset, (100, 200, 255))
        y_offset -= line_height
        controls = [
            "SPACE: Launch",
            "R: Reset",
            "TAB: Next Object",
            "Q/A: H-Angle +/-",
            "W/S: V-Angle +/-",
            "E/D: Force +/-",
            "Mouse: Rotate View",
            "Scroll: Zoom",
            "Arrows: Pan",
        ]
        for control in controls:
            self.draw_ui_text(control, x_offset, y_offset, (200, 200, 200), self.small_font)
            y_offset -= 20
            
    def handle_input(self):
        """Handle user input"""
        keys = pygame.key.get_pressed()
        
        # Angle and force adjustments
        if keys[pygame.K_q]:
            self.launch_angle_h += 1
            self.launch_angle_h = self.launch_angle_h % 360
        if keys[pygame.K_a]:
            self.launch_angle_h -= 1
            self.launch_angle_h = self.launch_angle_h % 360
        if keys[pygame.K_w]:
            self.launch_angle_v += 0.5
            self.launch_angle_v = min(90, self.launch_angle_v)
        if keys[pygame.K_s]:
            self.launch_angle_v -= 0.5
            self.launch_angle_v = max(-90, self.launch_angle_v)
        if keys[pygame.K_e]:
            self.launch_force += 0.5
            self.launch_force = min(200, self.launch_force)
        if keys[pygame.K_d]:
            self.launch_force -= 0.5
            self.launch_force = max(1, self.launch_force)
            
        # Camera panning with arrow keys
        pan_speed = 0.1
        if keys[pygame.K_LEFT]:
            self.camera.pan(-pan_speed, 0)
        if keys[pygame.K_RIGHT]:
            self.camera.pan(pan_speed, 0)
        if keys[pygame.K_UP]:
            self.camera.pan(0, -pan_speed)
        if keys[pygame.K_DOWN]:
            self.camera.pan(0, pan_speed)
            
    def run(self):
        """Main simulation loop"""
        running = True
        
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and not self.is_simulating:
                        # Launch object
                        self.is_simulating = True
                        self.current_object.apply_force(
                            self.launch_force, 
                            self.launch_angle_h, 
                            self.launch_angle_v
                        )
                    elif event.key == pygame.K_r:
                        # Reset
                        self.is_simulating = False
                        self.current_object.reset([0, 2, 0])
                    elif event.key == pygame.K_TAB:
                        # Next object
                        if not self.is_simulating:
                            self.object_type_index = (self.object_type_index + 1) % len(self.object_types)
                            self.current_object = Object3D(self.object_types[self.object_type_index])
                            self.current_object.reset([0, 2, 0])
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.mouse_pressed = True
                        self.last_mouse_pos = pygame.mouse.get_pos()
                    elif event.button == 4:  # Scroll up
                        self.camera.zoom(-0.5)
                    elif event.button == 5:  # Scroll down
                        self.camera.zoom(0.5)
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_pressed = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_pressed:
                        mouse_pos = pygame.mouse.get_pos()
                        dx = mouse_pos[0] - self.last_mouse_pos[0]
                        dy = mouse_pos[1] - self.last_mouse_pos[1]
                        self.camera.rotate(dx * 0.3, -dy * 0.3)
                        self.last_mouse_pos = mouse_pos
                        
            # Handle continuous input
            self.handle_input()
            
            # Update physics
            if self.is_simulating:
                still_moving = self.current_object.update(dt)
                if not still_moving:
                    self.is_simulating = False
                    
            # Get cursor 3D position
            mouse_pos = pygame.mouse.get_pos()
            self.cursor_3d_pos = self.get_cursor_3d_position(mouse_pos)
            
            # Render
            glClearColor(*COLORS['background'], 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            glLoadIdentity()
            self.camera.apply()
            
            # Draw scene
            self.draw_grid()
            self.draw_axes()
            self.current_object.draw()
            self.current_object.draw_trajectory()
            
            # Draw UI
            self.draw_ui()
            
            pygame.display.flip()
            
        pygame.quit()


def main():
    """Main entry point"""
    simulator = PhysicsSimulator()
    simulator.run()


if __name__ == "__main__":
    main()
