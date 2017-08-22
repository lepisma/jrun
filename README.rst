=============================
jrun
=============================

Run jupyter notebooks as command line scripts with variable overrides

For making variables overridable, wrap them using ``jin`` as shown below

.. code-block:: python

   from jrun import jin

   # First parameter is identifier, second is default value
   seed = jin("seed", 1234)
   speed = jin("speed", 45)
   trial_number = jin("tno", 1)

   # Other code

Running the notebook directly (``jrun notebook.ipynb``)  will use the default
parameter values. To override any of them, pass another argument to jrun
specifying the override in plain python like ``jrun notebook.ipynb "tno = 2;
seed = 2313"``.
