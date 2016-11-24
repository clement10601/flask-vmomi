# flask-vmomi
flask pyvmomi extension for vmware vsphere / vcenter access

    git clone [flask-vmomi]
    git install .

Usage:

    from flaskext.vmomi import Vmomi
    
    #app.py
    si = Vmomi(app).connect()

    #view
    from app import si
