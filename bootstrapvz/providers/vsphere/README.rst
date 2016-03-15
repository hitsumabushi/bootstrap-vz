vSphere
=========

The `vSphere <http://www.vmware.com/products/vsphere>`__ provider creates
virtual images for vSphere-based Virtual Machines. It supports the two type of
guest operating system module installation support, an official VMware Tools and
an `open-vm-tools <https://github.com/vmware/open-vm-tools>`__.

For overview of VMware Tools, see
`Overview of VMware Tools (340) <https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=340>`__.


Manifest settings
-----------------

Provider
~~~~~~~~

- ``vmware_tools``: Module installation setting
  ``optional``
   - ``tools_type``: Specifies which type of module install.
     ``optional``
   - ``path``: Specifies the path to VMware Tools tar.gz.
     This should be given, when select VMware tools installation.
     ``optional``

- ``vmdk_convert``: Specifies the path to vmdk-convert command.
  This command is built by `open-vmdk <https://github.com/vmware/open-vmdk>`.

Example:

.. code-block:: yaml

    ---
    provider:
      name: vsphere
      vmware_tools:
         tools_type: vmware-tools
         path: /path/to/vmware-toools.tgz
      vmdk_convert: /path/to/vmdk-convert

