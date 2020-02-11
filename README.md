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
