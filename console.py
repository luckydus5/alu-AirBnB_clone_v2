#!/usr/bin/python3
"""Command interpreter for managing AirBnB clone objects (v2)."""
import cmd
import shlex

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Interactive command interpreter for the AirBnB clone."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal (Ctrl-D) exits the program."""
        print("")
        return True

    @staticmethod
    def _cast(value):
        """Cast a create parameter token to int, float or unescaped string."""
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1].replace('\\"', '"').replace("_", " ")
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            return None

    def do_create(self, arg):
        """Create a new instance with optional parameters, save and print id.

        Usage: create <class name> [<key>=<value> ...]
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        cls_name = args[0]
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        params = {}
        for token in args[1:]:
            if "=" not in token:
                continue
            key, _, raw = token.partition("=")
            value = self._cast(raw)
            if value is not None:
                params[key] = value
        instance = HBNBCommand.classes[cls_name](**params)
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Print the string representation of an instance.

        Usage: show <class name> <id>
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        print(objects[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id.

        Usage: destroy <class name> <id>
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        objects[key].delete()
        storage.save()

    def do_all(self, arg):
        """Print all string representations of instances.

        Usage: all [<class name>]
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print([str(obj) for obj in storage.all().values()])
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in storage.all(args[0]).values()])

    def do_update(self, arg):
        """Update an instance by adding or modifying an attribute.

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        value = args[3]
        if attr_name in ("id", "created_at", "updated_at"):
            return
        obj = objects[key]
        current = getattr(obj, attr_name, None)
        if current is not None and not isinstance(current, str):
            try:
                value = type(current)(value)
            except (ValueError, TypeError):
                return
        setattr(obj, attr_name, value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
