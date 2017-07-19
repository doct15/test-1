################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Template Tag Flexibility to assign functionality per group.         ##
################################################################################


# -*- coding:utf-8 -*-
from __future__ import unicode_literals

################################################################################
## Import Required Python Libraries.                                          ##
################################################################################
from django import template



################################################################################
## Import Third Party Models.                                                 ##
################################################################################


################################################################################
## Instructions.                                                              ##
################################################################################
## To call in the template itself:
## {% load user_tags %} in the template.

## {% if request.user|has_group:"Administradores"%}
##     <div> Admins can see everything </div>
## {% endif %}

## check if in groupA or groupB for example
## user.groups.all.0.name == "groupname"



################################################################################
## Define The Group Tag Functionality.                                        ##
################################################################################
register = template.Library()

@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se este usuário pertence a um grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False
