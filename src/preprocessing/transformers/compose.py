
class Compose:

    def __init__(self, transfomations):
        self.transformations = transfomations

    def __call__(self, image):
        for transform in self.transformations:
            image = transform(image)
        return image