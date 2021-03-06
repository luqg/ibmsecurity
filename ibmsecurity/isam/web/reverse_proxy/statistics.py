import logging
#import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/reverseproxy"


def get_all(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving all statistics components and details - Reverse Proxy
    """
    try:
        return isamAppliance.invoke_get("Retrieving all statistics components - Reverse Proxy",
                                        "{0}/{1}/statistics".format(uri, instance_id))
    except:
        # Return empty array - exception thrown if list has no entries or does not exist
        ret_obj = isamAppliance.create_return_object()
        ret_obj['data'] = {}
        return ret_obj


def get_all_logs(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Retrieving all log files for a component - Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieving all statistics log files for a component - Reverse Proxy",
                                    "{0}/{1}/statistics/{2}/stats_files".format(uri,
                                                                         instance_id,
                                                                         component_id))


def get(isamAppliance, instance_id, component_id, file_id, options=None,
        size=None, start=None, check_mode=False, force=False):
    """
    Retrieving snippets of a statistics log file for a component - Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieving snippet of a statistics log file - Reverse Proxy",
                                    "{0}/{1}/statistics/{2}/stats_files/{3}".format(uri,
                                                                             instance_id,
                                                                             component_id,
                                                                             file_id,
                                                                             tools.create_query_string(
                                                options=options, start=start, size=size)))


def export_file(isamAppliance, instance_id, component_id, file_id, filename, check_mode=False, force=False):
    """
    Exporting a statistics log file for a component - Reverse Proxy
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file("Exporting a Reverse Proxy statistics log file.",
                                    "{0}/{1}/statistics/{2}/stats_files/{3}?export".format(uri,
                                                                             instance_id,
                                                                             component_id,
                                                                             file_id), filename)
    return isamAppliance.create_return_object()


def set(isamAppliance, instance_id, component_id, status, hours, mins, secs,
        count, flush_interval, rollover_size, max_rollover_files, compress,
        check_mode=False, force=False):
    """
    Modify the statistics settings for a component
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
                "Modify statistics settings for a component",
                "{0}/{1}/statistics/{2}".format(uri,
                                                instance_id,
                                                component_id),
                {
                    'status': status,
                    'interval_hours': hours,
                    'interval_mins': mins,
                    'interval_secs': secs,
                    'count': count,
                    'flush_interval': flush_interval,
                    'rollover_size': rollover_size,
                    'max_rollover_files': max_rollover_files,
                    'compress': compress

                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, instance_id, component_id, file_id, check_mode=False, force=False):
    """
    Deleting the statistics log file or rollover file for a component - Reverse Proxy
    """
    if force is False:
        try:
            ret_obj = get_default_snippet(isamAppliance, instance_id, component_id, file_id)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a statistics log file",
                "{0}/{1}/statistics/{2}/stats_files/{3}".format(uri,
                                                        instance_id,
                                                        component_id,
                                                        file_id))

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Deleting all the log files for a component - Reverse Proxy
    """
    if force is False:
        try:
            ret_obj = get_all_logs(isamAppliance, instance_id, component_id)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting all statistics log files",
                "{0}/{1}/statistics/{2}/stats_files".format(uri,
                                                        instance_id,
                                                        component_id))

    return isamAppliance.create_return_object()
