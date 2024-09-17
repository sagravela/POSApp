import os, sys

def get_resource_path(relative_path: str) -> str:
    """
    Resolves the absolute path for resources, considering whether the application is bundled with PyInstaller.

    This function adjusts the path resolution depending on whether the code is running in a PyInstaller bundle 
    or a development environment. It ensures that the correct path to resources is used in both scenarios.

    Parameters
    ----------
    relative_path : str
        The relative path to the resource within the application directory.

    Returns
    -------
    str
        The absolute path to the resource, adjusted for the application’s running context (bundled or development).
    """
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in a development environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
