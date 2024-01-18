#!/usr/bin/python3
"""command line interpreter for testing and debugging"""

import cmd
from models import classes
from models import storage
import re


def cne():
    """prints error message"""
    print("** class doesn't exist **")


def cnm():
    """prints error messages"""
    print("** class name missing **")


def idm():
    """prints error messages"""
    print("** instance id missing **")


def nif():
    """prints error messages"""
    print("** no instance found **")


def anm():
    """prints error messages"""
    print("** attribute name missing **")


def vm():
    """prints error messages"""
    print("** value missing **")


def list_instances(my_dict):
    """returns list of string represenations of all
    instances in the __objects dictionary"""
    list_ = []
    for key in my_dict.keys():
        obj = my_dict[key]
        list_.append(str(obj))
    return list_


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """end-of-file marker"""
        return True

    def emptyline(self):
        """default function called when enter is pressed
        on an empty line"""
        pass

    def do_create(self, line):
        """command handler for the create command
        that creates a new BaseModel instance"""
        args_list = line.split()
        len_ = len(args_list)
        try:
            if args_list[0] in classes:
                my_obj = classes[args_list[0]]()
                for i in range(1, len_):
                    param = args_list[i]
                    key_value = param.split('=')
                    if len(key_value) != 2:
                        continue
                    if (key_value[0] == "" or key_value[1] == ""):
                        continue
                    key = key_value[0]
                    value = eval(key_value[1])
                    if type(value) not in [str, float, int]:
                        continue
                    if type(value) is str:
                        value = value.replace("_", " ")
                    my_obj.set_attribute(key, value)
                my_obj.save()
                print(my_obj.id)
            else:
                cne()
        except IndexError:
            cnm()

    def do_show(self, line):
        """displays the string representaion of an instance"""
        args = line.split()
        try:
            if args[0] in classes:
                try:
                    key = f"{args[0]}.{args[1]}"
                    my_dict = storage.all()
                    if key in my_dict:
                        print(my_dict[key])
                    else:
                        nif()
                except IndexError:
                    idm()
            else:
                cne()
        except IndexError:
            cnm()

    def do_destroy(self, line):
        """destroys an instance and updates the json file"""
        args = line.split()
        try:
            if args[0] in classes:
                try:
                    key = f"{args[0]}.{args[1]}"
                    my_dict = storage.all()
                    if key in my_dict:
                        del my_dict[key]
                        storage.save()
                    else:
                        nif()
                except IndexError:
                    idm()
            else:
                cne()
        except IndexError:
            cnm()

    def do_all(self, line):
        """prints the list of string representations of all
        instances"""
        args = line.split()
        my_dict = storage.all()
        my_list = []
        try:
            if args[0] in classes:
                for key in my_dict:
                    to_dict = storage.all()[key].to_dict()
                    if args[0] == to_dict["__class__"]:
                        my_list.append(str(storage.all()[key]))
                print(my_list)
            else:
                cne()
        except IndexError:
            my_list = list_instances(my_dict)
            print(my_list)

    def do_update(self, line):
        """updates an attribute of an instance with a new value"""
        args = line.split()
        try:
            if args[0] in classes:
                try:
                    key = f"{args[0]}.{args[1]}"
                    my_dict = storage.all()
                    if key in my_dict:
                        try:
                            if args[2]:
                                try:
                                    value = args[3]
                                    obj = my_dict[key]
                                    obj.set_attribute(args[2], eval(value))
                                    obj.save()
                                except IndexError:
                                    vm()
                        except IndexError:
                            anm()
                    else:
                        nif()
                except IndexError:
                    idm()
            else:
                cne()
        except IndexError:
            cnm()

    def default(self, line):
        """Default Method called"""
        args = line.split(".")
        if args[1] == "all()":
            self.do_all(args[0])
        elif args[1] == "count()":
            count = 0
            for key in storage.all().keys():
                to_dict = storage.all()[key].to_dict()
                if args[0] == to_dict["__class__"]:
                    count += 1
            print(count)
        elif args[1].startswith("show("):
            reg = re.compile('"([^"]*)"')
            id_ = reg.search(args[1])
            self.do_show(f"{args[0]} {id_.group()[1:-1]}")
        elif args[1].startswith("destroy("):
            reg = re.compile('"([^"]*)"')
            id_ = reg.search(args[1])
            self.do_destroy(f"{args[0]} {id_.group()[1:-1]}")
        elif args[1].startswith("update("):
            reg = re.compile(r'\((.*?)\)')
            str_ = reg.search(args[1])
            str_ = str_.group()[1:-1].split(", ")
            if args[0] in classes:
                try:
                    key = f"{args[0]}.{str_[0][1:-1]}"
                    my_dict = storage.all()
                    if key in my_dict:
                        try:
                            if str_[1]:
                                try:
                                    value = str_[2]
                                    obj = my_dict[key]
                                    arg1 = f"{str_[1][1:-1]}"
                                    arg2 = f"{eval(value)}"
                                    obj.set_attribute(arg1, arg2)
                                    obj.save()
                                except IndexError:
                                    vm()
                        except IndexError:
                            anm()
                    else:
                        nif()
                except IndexError:
                    idm()
            else:
                cne()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
