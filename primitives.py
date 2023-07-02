import pygame


# Super class - representing objects that can be drawn on the screen
class DrawableObject:
    def __init__(self, x, y, w, h, rotation=0):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.object_name = "Drawable"
        self.rotation = rotation

    def get_type(self):
        return self.object_name

    def draw(self, context: pygame.display):
        pygame.draw.circle(context, self.x, self.y, 100)


# Derived class - representing an ellipse object 
class Ellipse(DrawableObject):
    def __init__(self, color, x, y, w, h, rotation=0):
        super().__init__(x, y, w, h, rotation)
        self.object_name = "Ellipse"
        self.color = color

    def draw(self, context: pygame.display):
        # Determine circle rect
        center = (self.x, self.y)
        rect = pygame.Rect(center[0] - self.width / 2,
                           center[1] - self.height / 2,
                           self.width,
                           self.height)

        # Create surface for rotated circle
        target_rect = pygame.Rect(rect)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, self.color, (0, 0, *target_rect.size), self.width)

        # Rotate circle
        rotated_surf = pygame.transform.rotate(shape_surf, self.rotation)

        # Draw circle
        context.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


# Derived class - representing a rectangular object
class Rectangle(DrawableObject):
    def __init__(self, color, x, y, w, h, rotation=0):
        super().__init__(x, y, w, h, rotation)
        self.object_name = "Rectangle"
        self.color = color

    def draw(self, context: pygame.display):
        # Create rect surface
        surface = pygame.Surface((self.width, self.height))
        surface.set_colorkey((0, 0, 0))
        surface.fill(self.color)

        # Convert surface to image
        image = surface.copy()

        # Rotate surface
        image = pygame.transform.rotate(image, self.rotation)
        rect = image.get_rect()
        rect.center = (self.x, self.y)

        # Draw surface
        context.blit(image, rect)


# Derived class - representing a text object
class Text(DrawableObject):
    def __init__(self, content, surface, color, x, y, w, h, rotation=0):
        super().__init__(x, y, w, h, rotation)
        self.object_name = "Text"
        self.color = color
        self.contents = content
        self.surface = surface

    def draw(self, context: pygame.display):
        # Rotate surface
        self.surface = pygame.transform.rotate(self.surface, self.rotation)
        rect = self.surface.get_rect()
        rect.center = (self.x, self.y)

        # Draw surface
        context.blit(self.surface, rect)


# Derived class - representing an image object
class Image(DrawableObject):
    def __init__(self, url, scale, x, y, rotation=0):
        super().__init__(x, y, None, None, rotation)
        self.object_name = "Image"
        self.url = url
        self.scale = scale

    # NOTE: image must be inside the assets folder
    def draw(self, context: pygame.display):
        image = pygame.image.load("assets/" + self.url)

        # Resize image
        w = image.get_width()
        h = image.get_height()
        new_size = (w * self.scale, h * self.scale)
        image = pygame.transform.scale(image, new_size)

        # Place image in center of specified coordinates
        image_rect = image.get_rect()
        image_rect.center = (self.x, self.y)

        # Rotate image
        image = pygame.transform.rotate(image, self.rotation)

        # Draw image
        context.blit(image, image_rect)


# Representing an audio object
class Audio:
    def __init__(self, channel: int, path: str):
        self.filepath = path
        self.channel = channel
