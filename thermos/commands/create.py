
"""The create command."""

from json import dumps

from .base import Base


class Create(Base):
    """Make base application folder structure"""

    def run(self):
        print("test")
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
