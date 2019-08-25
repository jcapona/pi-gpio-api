Raspberry Pi GPIO Api
=====================


API to access Raspberry Pi GPIO based on Python & Flask

Outputs
-------

To access and set the status of an output, a POST request must be sent to `/api/gpio/output/<OUTPUT>`, where OUTPUT is the index used to identify the output pin.
The content of the POST message must be in a valid json format, in the form:

.. code-block:: sh

    {"value": 1}


With a 1 or a 0 as the value. An `Ok` should be received on success, or a message detailing the error on failure.

Inputs
------

To set a channel as an input and read the current status, a GET request must be sent to `/api/gpio/input/<INPUT>`, where `INPUT` is the index of the pin to be read.

Status
------

To read the status of all the IO modified in the current session, a GET request must be sent to `/api/gpio/info`.

