#!/usr/bin/python3
# -*- coding: utf-8 -*-
global global_public_ip


def set_value(value):

    global global_public_ip
    global_public_ip = value


def get_value():

    global global_public_ip
    return global_public_ip