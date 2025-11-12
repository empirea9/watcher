"""
3D Projectile Motion Simulator
Enhanced version with GUI controls and drag functionality
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import pygame_gui

# Color scheme - dark aesthetic with black, white, gray, blue, and yellow
COLORS = {
    'background': (0.05, 0.05, 0.05),  # Almost black
    'grid': (0.2, 0.2, 0.2),  # Dark gray
    'trajectory': (0.3, 0.6, 1.0),  # Blue
    'object': (0.9, 0.9, 0.9),  # Light gray/white
    'object_dragging': (1.0, 0.9, 0.2),  # Yellow when dragging
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
        
        # Trajectory tracking with time and velocity
        self.trajectory = []
        self.trajectory_data = []  # Stores (position, velocity, time)
        self.simulation_time = 0.0
        
        # Velocity components for display
        self.h_velocity_magnitude = 0.0
        self.v_velocity_magnitude = 0.0
        
        # Drag state
        self.is_being_dragged = False
        
    def reset(self, position):
        """Reset object to initial position"""
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.angular_velocity = np.array([0.0, 0.0, 0.0])
        self.trajectory = [self.position.copy()]
        self.trajectory_data = [(self.position.copy(), self.velocity.copy(), 0.0)]
        self.simulation_time = 0.0
        
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
        if self.is_being_dragged:
            return True
            
        # Apply gravity
        self.velocity[1] += gravity * dt
        
        # Update position
        self.position += self.velocity * dt
        
        # Update rotation
        self.rotation += self.angular_velocity * dt
        
        # Update simulation time
        self.simulation_time += dt
        
        # Store trajectory point with time and velocity data
        if len(self.trajectory) == 0 or np.linalg.norm(self.position - self.trajectory[-1]) > 0.1:
            self.trajectory.append(self.position.copy())
            self.trajectory_data.append((self.position.copy(), self.velocity.copy(), self.simulation_time))
        
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
        
        if self.is_being_dragged:
            glColor3f(*COLORS['object_dragging'])
        else:
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
        
    def draw_velocity_arrows(self):
        """Draw velocity arrows showing horizontal and vertical components"""
        if self.is_being_dragged or np.linalg.norm(self.velocity) < 0.1:
            return
            
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        # Lighter shade for velocity arrows (semi-transparent)
        arrow_length_scale = 0.5
        
        # Horizontal velocity (XZ plane)
        v_horizontal = np.array([self.velocity[0], 0, self.velocity[2]])
        self.h_velocity_magnitude = np.linalg.norm(v_horizontal)
        if self.h_velocity_magnitude > 0.1:
            h_dir = v_horizontal / self.h_velocity_magnitude
            h_length = self.h_velocity_magnitude * arrow_length_scale
            
            glColor4f(1.0, 0.8, 0.2, 0.7)  # Yellow-ish, lighter
            glLineWidth(2.5)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(h_dir[0] * h_length, 0, h_dir[2] * h_length)
            glEnd()
            
            # Arrow head for horizontal
            self._draw_arrow_head(h_dir[0] * h_length, 0, h_dir[2] * h_length, h_dir, 0.2)
        
        # Vertical velocity (Y axis)
        self.v_velocity_magnitude = abs(self.velocity[1])
        if self.v_velocity_magnitude > 0.1:
            v_length = self.velocity[1] * arrow_length_scale
            v_dir = 1 if self.velocity[1] > 0 else -1
            
            glColor4f(0.2, 1.0, 0.4, 0.7)  # Green-ish, lighter
            glLineWidth(2.5)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(0, v_length, 0)
            glEnd()
            
            # Arrow head for vertical
            self._draw_arrow_head(0, v_length, 0, np.array([0, v_dir, 0]), 0.2)
        
        glLineWidth(1.0)
        glPopMatrix()
        
    def _draw_arrow_head(self, x, y, z, direction, size):
        """Draw an arrow head at the specified position"""
        # Simple cone for arrow head
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Rotate to point in the direction
        if direction[1] != 0:  # Vertical arrow
            angle = 0 if direction[1] > 0 else 180
            glRotatef(angle, 1, 0, 0)
        else:  # Horizontal arrow
            angle = math.degrees(math.atan2(direction[2], direction[0]))
            glRotatef(angle, 0, 1, 0)
            glRotatef(90, 0, 0, 1)
        
        quadric = gluNewQuadric()
        gluCylinder(quadric, size, 0, size * 2, 8, 8)
        gluDeleteQuadric(quadric)
        
        glPopMatrix()


class Camera:
    """3D Camera with movement controls"""
    
    def __init__(self):
        self.position = np.array([10.0, 5.0, 10.0])
        self.target = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.yaw = -135.0
        self.pitch = -20.0
        self.distance = 15.0
        self.speed = 0.3  # Increased default camera speed
        
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
        self.distance = max(2, min(100, self.distance))
        self.update_position()
        
    def pan(self, forward, right):
        """Pan camera target - fixed to use proper forward/right movement"""
        yaw_rad = math.radians(self.yaw)
        
        # Forward direction (based on yaw) - inverted for intuitive controls
        forward_x = -math.cos(yaw_rad)
        forward_z = -math.sin(yaw_rad)
        
        # Right direction (perpendicular to forward)
        right_x = math.sin(yaw_rad)
        right_z = -math.cos(yaw_rad)
        
        # Apply movement with camera speed
        self.target[0] += (forward * forward_x + right * right_x) * self.speed
        self.target[2] += (forward * forward_z + right * right_z) * self.speed
        
        self.update_position()


class PhysicsSimulator:
    """Main physics simulator application with GUI controls"""
    
    def __init__(self, width=1400, height=800):
        pygame.init()
        self.width = width
        self.height = height
        
        # Create OpenGL display
        self.display = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Projectile Motion Simulator - Enhanced")
        
        # Create a surface for GUI rendering (pygame_gui needs a regular pygame surface)
        self.gui_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # OpenGL setup
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Projection
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 500.0)  # Increased far plane for infinite grid
        glMatrixMode(GL_MODELVIEW)
        
        # Camera
        self.camera = Camera()
        
        # GUI Manager - use the gui_surface instead of display
        self.gui_manager = pygame_gui.UIManager((width, height), 'theme.json')
        
        # Simulation state
        self.current_object = Object3D('football')
        self.current_object.reset([0, 2, 0])
        self.object_types = list(Object3D.OBJECTS.keys())
        
        self.is_simulating = False
        self.launch_angle_h = 45.0
        self.launch_angle_v = 45.0
        self.launch_force = 20.0
        
        # Timeline state
        self.timeline_scrubbing = False
        self.timeline_position = 0.0  # 0.0 to 1.0
        
        # Mouse control for camera
        self.camera_rotating = False
        self.last_mouse_pos = (0, 0)
        
        # Object dragging
        self.dragging_object = False
        self.drag_plane_distance = 10.0
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # Create GUI elements
        self.create_gui()
        
    def create_gui(self):
        """Create GUI controls with sliders"""
        panel_width = 320
        panel_x = self.width - panel_width - 10
        y_offset = 10
        element_height = 30
        spacing = 8
        label_height = 25
        
        # Title
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, 30)),
            text='<b>PROJECTILE SIMULATOR</b>',
            manager=self.gui_manager
        )
        y_offset += 40
        
        # Object selection dropdown
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, label_height)),
            text='Select Object:',
            manager=self.gui_manager
        )
        y_offset += label_height + 3
        
        self.object_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=[Object3D.OBJECTS[k]['name'] for k in self.object_types],
            starting_option='Football',
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            manager=self.gui_manager
        )
        y_offset += element_height + spacing + 5
        
        # Horizontal angle with slider and text input
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, label_height)),
            text='Horizontal Angle (0-360°):',
            manager=self.gui_manager
        )
        y_offset += label_height + 3
        
        self.h_angle_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            start_value=45.0,
            value_range=(0.0, 360.0),
            manager=self.gui_manager
        )
        y_offset += element_height + 3
        
        self.h_angle_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            manager=self.gui_manager
        )
        self.h_angle_entry.set_text('45.0')
        y_offset += element_height + spacing
        
        # Vertical angle with slider and text input
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, label_height)),
            text='Vertical Angle (-90 to 90°):',
            manager=self.gui_manager
        )
        y_offset += label_height + 3
        
        self.v_angle_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            start_value=45.0,
            value_range=(-90.0, 90.0),
            manager=self.gui_manager
        )
        y_offset += element_height + 3
        
        self.v_angle_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            manager=self.gui_manager
        )
        self.v_angle_entry.set_text('45.0')
        y_offset += element_height + spacing
        
        # Force input
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, label_height)),
            text='Launch Force (1-200 N):',
            manager=self.gui_manager
        )
        y_offset += label_height + 3
        
        self.force_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            manager=self.gui_manager
        )
        self.force_entry.set_text('20.0')
        y_offset += element_height + spacing
        
        # Camera speed slider
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, label_height)),
            text='Camera Speed:',
            manager=self.gui_manager
        )
        y_offset += label_height + 3
        
        self.camera_speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, element_height)),
            start_value=0.3,
            value_range=(0.1, 2.0),
            manager=self.gui_manager
        )
        y_offset += element_height + spacing + 5
        
        # Launch button
        self.launch_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, 40)),
            text='LAUNCH',
            manager=self.gui_manager
        )
        y_offset += 45
        
        # Reset button
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, 40)),
            text='RESET',
            manager=self.gui_manager
        )
        y_offset += 50
        
        # Info label
        self.info_label = pygame_gui.elements.UITextBox(
            html_text='<font color="#CCCCCC" size="3"><b>Controls:</b><br>• Right-click: Drag object<br>• Left-click: Rotate camera<br>• Arrow keys: Pan camera<br>• Scroll: Zoom<br>• Q/A: H-Angle +/-<br>• W/S: V-Angle +/-</font>',
            relative_rect=pygame.Rect((panel_x, y_offset), (panel_width, 140)),
            manager=self.gui_manager
        )
        
    def draw_infinite_grid(self):
        """Draw infinite grid that follows camera"""
        # Get camera target position
        cx, cz = self.camera.target[0], self.camera.target[2]
        
        # Calculate grid bounds based on camera position
        grid_size = 100  # Extended grid size
        spacing = 2
        
        # Round to nearest grid unit
        start_x = int((cx - grid_size) / spacing) * spacing
        end_x = int((cx + grid_size) / spacing) * spacing
        start_z = int((cz - grid_size) / spacing) * spacing
        end_z = int((cz + grid_size) / spacing) * spacing
        
        glColor3f(*COLORS['grid'])
        glBegin(GL_LINES)
        
        # Draw lines parallel to X axis
        for z in range(start_z, end_z + 1, spacing):
            glVertex3f(start_x, 0, z)
            glVertex3f(end_x, 0, z)
        
        # Draw lines parallel to Z axis
        for x in range(start_x, end_x + 1, spacing):
            glVertex3f(x, 0, start_z)
            glVertex3f(x, 0, end_z)
        
        glEnd()
        
    def draw_axes(self, length=5, position=None):
        """Draw coordinate axes at specified position or origin"""
        if position is None:
            position = [0, 0, 0]
            
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        
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
        glPopMatrix()
        
    def get_3d_pos_from_mouse(self, mouse_pos, distance):
        """Convert 2D mouse position to 3D world coordinates at a specific distance"""
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        
        x = mouse_pos[0]
        y = viewport[3] - mouse_pos[1]
        
        # Unproject at specific depth
        pos_near = gluUnProject(x, y, 0.0, modelview, projection, viewport)
        pos_far = gluUnProject(x, y, 1.0, modelview, projection, viewport)
        
        # Calculate ray direction
        ray_dir = np.array([pos_far[0] - pos_near[0], 
                           pos_far[1] - pos_near[1], 
                           pos_far[2] - pos_near[2]])
        ray_dir = ray_dir / np.linalg.norm(ray_dir)
        
        # Calculate intersection with plane at distance from camera
        camera_pos = np.array(self.camera.position)
        target_pos = camera_pos + ray_dir * distance
        
        return target_pos
        
    def is_mouse_over_object(self, mouse_pos):
        """Check if mouse is over the 3D object"""
        # Simple distance check in screen space
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        
        try:
            # Project object position to screen
            screen_pos = gluProject(
                self.current_object.position[0],
                self.current_object.position[1],
                self.current_object.position[2],
                modelview, projection, viewport
            )
            
            # Check distance in screen space
            dx = mouse_pos[0] - screen_pos[0]
            dy = (viewport[3] - mouse_pos[1]) - screen_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Threshold based on object size and distance
            threshold = 50  # pixels
            return distance < threshold
        except:
            return False
            
    def handle_gui_events(self, event):
        """Handle GUI events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.launch_button and not self.is_simulating:
                # Read values from GUI
                try:
                    self.launch_angle_h = float(self.h_angle_entry.get_text())
                    self.launch_angle_v = float(self.v_angle_entry.get_text())
                    self.launch_force = float(self.force_entry.get_text())
                    
                    # Clamp values
                    self.launch_angle_h = self.launch_angle_h % 360
                    self.launch_angle_v = max(-90, min(90, self.launch_angle_v))
                    self.launch_force = max(1, min(200, self.launch_force))
                    
                    # Launch
                    self.is_simulating = True
                    self.current_object.is_being_dragged = False
                    self.current_object.apply_force(
                        self.launch_force,
                        self.launch_angle_h,
                        self.launch_angle_v
                    )
                except ValueError:
                    pass  # Invalid input
                    
            elif event.ui_element == self.reset_button:
                self.is_simulating = False
                self.current_object.reset([0, 2, 0])
                self.current_object.is_being_dragged = False
                
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.object_dropdown and not self.is_simulating:
                # Find object type by name
                selected_name = event.text
                for obj_type, data in Object3D.OBJECTS.items():
                    if data['name'] == selected_name:
                        self.current_object = Object3D(obj_type)
                        self.current_object.reset([0, 2, 0])
                        break
                        
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.camera_speed_slider:
                self.camera.speed = event.value
            elif event.ui_element == self.h_angle_slider:
                # Update text entry when slider moves
                self.launch_angle_h = event.value
                self.h_angle_entry.set_text(f'{event.value:.1f}')
            elif event.ui_element == self.v_angle_slider:
                # Update text entry when slider moves
                self.launch_angle_v = event.value
                self.v_angle_entry.set_text(f'{event.value:.1f}')
                
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            # Update sliders when text entry changes
            if event.ui_element == self.h_angle_entry:
                try:
                    value = float(event.text)
                    value = value % 360
                    self.h_angle_slider.set_current_value(value)
                    self.launch_angle_h = value
                except ValueError:
                    pass
            elif event.ui_element == self.v_angle_entry:
                try:
                    value = float(event.text)
                    value = max(-90, min(90, value))
                    self.v_angle_slider.set_current_value(value)
                    self.launch_angle_v = value
                except ValueError:
                    pass
    
    def draw_velocity_labels(self):
        """Draw velocity component labels on the object"""
        if self.current_object.is_being_dragged or np.linalg.norm(self.current_object.velocity) < 0.1:
            return
        
        # Get 3D position of object
        obj_pos = self.current_object.position
        
        # Project 3D position to 2D screen coordinates
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        try:
            from OpenGL.GLU import gluProject
            screen_coords = gluProject(obj_pos[0], obj_pos[1], obj_pos[2], modelview, projection, viewport)
            screen_x = int(screen_coords[0])
            screen_y = int(self.height - screen_coords[1])  # Flip Y coordinate
            
            # Draw labels near the object
            font = pygame.font.Font(None, 20)
            
            # Horizontal velocity label (yellow)
            if hasattr(self.current_object, 'h_velocity_magnitude') and self.current_object.h_velocity_magnitude > 0.1:
                h_text = font.render(f"vₕ={self.current_object.h_velocity_magnitude:.2f} m/s", True, (255, 200, 50))
                self.gui_surface.blit(h_text, (screen_x + 15, screen_y - 30))
            
            # Vertical velocity label (green)
            if hasattr(self.current_object, 'v_velocity_magnitude') and self.current_object.v_velocity_magnitude > 0.1:
                v_text = font.render(f"vᵥ={self.current_object.v_velocity_magnitude:.2f} m/s", True, (50, 255, 100))
                self.gui_surface.blit(v_text, (screen_x + 15, screen_y - 10))
                
        except Exception:
            pass  # Skip if projection fails
    
    def draw_timeline(self):
        """Draw timeline UI at the bottom of the screen to scrub through trajectory"""
        if len(self.current_object.trajectory_data) < 2:
            return
        
        # Timeline dimensions
        timeline_height = 60
        timeline_y = self.height - timeline_height
        timeline_margin = 20
        timeline_width = self.width - 2 * timeline_margin
        timeline_x = timeline_margin
        
        # Draw on GUI surface (2D overlay)
        import pygame.draw as draw
        
        # Draw timeline background (dark bar)
        timeline_rect = pygame.Rect(timeline_x, timeline_y, timeline_width, timeline_height)
        draw.rect(self.gui_surface, (10, 10, 10, 200), timeline_rect)
        draw.rect(self.gui_surface, (50, 50, 50), timeline_rect, 2)
        
        # Draw trajectory points as dots
        max_time = self.current_object.trajectory_data[-1][2] if len(self.current_object.trajectory_data) > 0 else 1.0
        for i, (pos, vel, time) in enumerate(self.current_object.trajectory_data):
            if max_time > 0:
                x_pos = timeline_x + int((time / max_time) * timeline_width)
                y_pos = timeline_y + timeline_height // 2
                
                # Color based on velocity magnitude
                vel_mag = np.linalg.norm(vel)
                color_intensity = min(255, int(vel_mag * 10))
                draw.circle(self.gui_surface, (color_intensity, 100, 255 - color_intensity), (x_pos, y_pos), 3)
        
        # Draw current position marker
        if not self.is_simulating and len(self.current_object.trajectory_data) > 1:
            current_time = self.current_object.simulation_time
            if max_time > 0:
                marker_x = timeline_x + int((current_time / max_time) * timeline_width)
                marker_y = timeline_y
                # Draw draggable marker handle (larger circle)
                draw.circle(self.gui_surface, (255, 255, 0), (marker_x, marker_y + timeline_height // 2), 8)
                draw.circle(self.gui_surface, (200, 200, 0), (marker_x, marker_y + timeline_height // 2), 6)
                # Draw vertical line marker
                draw.line(self.gui_surface, (255, 255, 0, 128), (marker_x, marker_y), (marker_x, marker_y + timeline_height), 2)
                
                # Find closest trajectory point for velocity display
                closest_idx = 0
                closest_dist = float('inf')
                for i, (pos, vel, time) in enumerate(self.current_object.trajectory_data):
                    dist = abs(time - current_time)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_idx = i
                
                if closest_idx < len(self.current_object.trajectory_data):
                    _, vel, _ = self.current_object.trajectory_data[closest_idx]
                    vel_mag = np.linalg.norm(vel)
                    v_horizontal = np.linalg.norm([vel[0], 0, vel[2]])
                    v_vertical = abs(vel[1])
                    
                    # Display velocity text with components
                    font = pygame.font.Font(None, 24)
                    vel_text = font.render(f"v={vel_mag:.2f} m/s  vₕ={v_horizontal:.2f} m/s  vᵥ={v_vertical:.2f} m/s  t={current_time:.2f}s", True, (255, 255, 255))
                    self.gui_surface.blit(vel_text, (timeline_x + 10, timeline_y + 5))
    
    def is_mouse_over_timeline_marker(self, mouse_pos):
        """Check if mouse is over the timeline marker"""
        if len(self.current_object.trajectory_data) < 2:
            return False
        
        timeline_height = 60
        timeline_y = self.height - timeline_height
        timeline_margin = 20
        timeline_width = self.width - 2 * timeline_margin
        timeline_x = timeline_margin
        
        max_time = self.current_object.trajectory_data[-1][2]
        current_time = self.current_object.simulation_time
        
        if max_time > 0:
            marker_x = timeline_x + int((current_time / max_time) * timeline_width)
            marker_y = timeline_y + timeline_height // 2
            
            # Check if mouse is within 10 pixels of marker
            dx = mouse_pos[0] - marker_x
            dy = mouse_pos[1] - marker_y
            distance = math.sqrt(dx*dx + dy*dy)
            return distance < 10
        
        return False
    
    def update_timeline_from_mouse(self, mouse_pos):
        """Update simulation time based on mouse position on timeline"""
        if len(self.current_object.trajectory_data) < 2:
            return
        
        timeline_height = 60
        timeline_y = self.height - timeline_height
        timeline_margin = 20
        timeline_width = self.width - 2 * timeline_margin
        timeline_x = timeline_margin
        
        # Clamp mouse position to timeline bounds
        relative_x = max(0, min(timeline_width, mouse_pos[0] - timeline_x))
        timeline_position = relative_x / timeline_width
        
        # Calculate new time
        max_time = self.current_object.trajectory_data[-1][2]
        new_time = timeline_position * max_time
        
        # Find closest trajectory point and update object state
        closest_idx = 0
        closest_dist = float('inf')
        for i, (pos, vel, time) in enumerate(self.current_object.trajectory_data):
            dist = abs(time - new_time)
            if dist < closest_dist:
                closest_dist = dist
                closest_idx = i
        
        if closest_idx < len(self.current_object.trajectory_data):
            pos, vel, time = self.current_object.trajectory_data[closest_idx]
            self.current_object.position = pos.copy()
            self.current_object.velocity = vel.copy()
            self.current_object.simulation_time = time
                
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
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if clicking on timeline marker (priority check)
                    if event.button == 1 and not self.is_simulating:
                        if self.is_mouse_over_timeline_marker(mouse_pos):
                            self.timeline_scrubbing = True
                        elif mouse_pos[0] < self.width - 320:  # Not on GUI panel
                            self.camera_rotating = True
                            self.last_mouse_pos = mouse_pos
                    elif mouse_pos[0] < self.width - 320:  # Not on GUI panel
                        if event.button == 3:  # Right click - drag object
                            if self.is_mouse_over_object(mouse_pos) and not self.is_simulating:
                                self.dragging_object = True
                                self.current_object.is_being_dragged = True
                                self.drag_plane_distance = np.linalg.norm(
                                    self.current_object.position - self.camera.position
                                )
                        elif event.button == 4:  # Scroll up
                            self.camera.zoom(-0.5)
                        elif event.button == 5:  # Scroll down
                            self.camera.zoom(0.5)
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.camera_rotating = False
                        self.timeline_scrubbing = False
                    elif event.button == 3:
                        self.dragging_object = False
                        self.current_object.is_being_dragged = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    if self.timeline_scrubbing:
                        mouse_pos = pygame.mouse.get_pos()
                        self.update_timeline_from_mouse(mouse_pos)
                    elif self.camera_rotating:
                        mouse_pos = pygame.mouse.get_pos()
                        dx = mouse_pos[0] - self.last_mouse_pos[0]
                        dy = mouse_pos[1] - self.last_mouse_pos[1]
                        self.camera.rotate(dx * 0.3, -dy * 0.3)
                        self.last_mouse_pos = mouse_pos
                    elif self.dragging_object:
                        mouse_pos = pygame.mouse.get_pos()
                        new_pos = self.get_3d_pos_from_mouse(mouse_pos, self.drag_plane_distance)
                        self.current_object.position = new_pos
                        self.current_object.trajectory = [self.current_object.position.copy()]
                        
                # Handle GUI events
                self.gui_manager.process_events(event)
                self.handle_gui_events(event)
            
            # Handle arrow key panning and angle keyboard controls
            keys = pygame.key.get_pressed()
            
            # Arrow keys for camera panning
            if keys[pygame.K_UP]:
                self.camera.pan(1, 0)  # Forward
            if keys[pygame.K_DOWN]:
                self.camera.pan(-1, 0)  # Backward
            if keys[pygame.K_LEFT]:
                self.camera.pan(0, -1)  # Left
            if keys[pygame.K_RIGHT]:
                self.camera.pan(0, 1)  # Right
            
            # Q/A keys for horizontal angle adjustment
            if keys[pygame.K_q]:
                self.launch_angle_h = (self.launch_angle_h + 1) % 360
                self.h_angle_slider.set_current_value(self.launch_angle_h)
                self.h_angle_entry.set_text(f'{self.launch_angle_h:.1f}')
            if keys[pygame.K_a]:
                self.launch_angle_h = (self.launch_angle_h - 1) % 360
                self.h_angle_slider.set_current_value(self.launch_angle_h)
                self.h_angle_entry.set_text(f'{self.launch_angle_h:.1f}')
            
            # W/S keys for vertical angle adjustment
            if keys[pygame.K_w]:
                self.launch_angle_v = min(90, self.launch_angle_v + 0.5)
                self.v_angle_slider.set_current_value(self.launch_angle_v)
                self.v_angle_entry.set_text(f'{self.launch_angle_v:.1f}')
            if keys[pygame.K_s]:
                self.launch_angle_v = max(-90, self.launch_angle_v - 0.5)
                self.v_angle_slider.set_current_value(self.launch_angle_v)
                self.v_angle_entry.set_text(f'{self.launch_angle_v:.1f}')
            
            # Update physics
            if self.is_simulating:
                still_moving = self.current_object.update(dt)
                if not still_moving:
                    self.is_simulating = False
            
            # Update GUI
            self.gui_manager.update(dt)
            
            # Render 3D scene with OpenGL
            glClearColor(*COLORS['background'], 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            glLoadIdentity()
            self.camera.apply()
            
            # Draw 3D scene
            self.draw_infinite_grid()
            self.draw_axes()  # Origin axes
            self.draw_axes(length=2, position=self.current_object.position)  # Axes at object position
            self.current_object.draw()
            self.current_object.draw_velocity_arrows()
            self.current_object.draw_trajectory()
            
            # Now render GUI on top
            # First, clear the GUI surface
            self.gui_surface.fill((0, 0, 0, 0))  # Transparent
            
            # Draw GUI to the surface
            self.gui_manager.draw_ui(self.gui_surface)
            
            # Draw velocity component labels on object
            self.draw_velocity_labels()
            
            # Draw timeline overlay
            self.draw_timeline()
            
            # Convert pygame surface to OpenGL texture and draw it
            # Switch to 2D orthographic projection
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.width, self.height, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            # Disable depth test for 2D overlay
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Convert surface to texture
            texture_data = pygame.image.tostring(self.gui_surface, 'RGBA', True)
            glEnable(GL_TEXTURE_2D)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            
            # Draw textured quad (fix inverted rendering by flipping V coordinate)
            glColor4f(1, 1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(0, 0)
            glTexCoord2f(1, 1); glVertex2f(self.width, 0)
            glTexCoord2f(1, 0); glVertex2f(self.width, self.height)
            glTexCoord2f(0, 0); glVertex2f(0, self.height)
            glEnd()
            
            # Cleanup
            glDeleteTextures([texture_id])
            glDisable(GL_TEXTURE_2D)
            
            # Restore 3D state
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            
            pygame.display.flip()
            
        pygame.quit()


def main():
    """Main entry point"""
    simulator = PhysicsSimulator()
    simulator.run()


if __name__ == "__main__":
    main()
