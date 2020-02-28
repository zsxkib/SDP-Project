# SDP Project
## Item Collector / Sorter

Attachment for bin that sorts any arbitrary trash that you throw in into specific bins using vision (to detect type of trash) and robotics (to "move" trash into corresponding bins).

### Demo1

The pi should communicate with the server using `WebClient`, as demostrated in `bin_server.py`

On the server, run `python3 web_server.py cfer.pkl` to set up the web interface and the model (provided by a pickle dump from training)

To train and test the model without hardware, run `train_and_test.py`.
Accuracy reported on the dataset might not correspond to the actual accuracy since

1) in the dataset we only have one image per item but on the bin we plan to have multiple images from different angles
2) the backgroud, lighting condition and distribution of wastes in our bin may differ from the dataset


### Trash photo website
tinyurl.com/recyclotron-upload

### How to start the machine
Since we had some difficulties to connect motor board and sensor board on the same pi, we now have two pis. To start the machine, first start the motor server on pi2:
```
ssh pi2@212.71.237.145
# after login:
cd SDP-Project/
python3 move_flask.py
```

Then, start the state machine script on the other pi (the main controller):
```
ssh pi@212.71.237.145
# after login:
cd SDP-Project/
python3 stateMachine.py
```
(The ultrasonic sensor sometimes breaks and reports crazy readings like 500 centimeters and as a result, recyclotron will move infinitely towards one end. Look out for such situations when running the script, reading numbers are logged on terminal)

Finally we need a classifier server (currently it's on my pc, if needed we can setup a backup plan on somebody else's computer or use a neural compute stick on pi to speed up the inference speed)
```
# on the compute server
cd SDP-Project/
python3 web_server2.py path_to_nn_model_dir threshold n_bins
```
