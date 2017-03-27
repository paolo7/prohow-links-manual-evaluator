# Manual Evaluator of PROHOW Links

The links file to manually evaluate needs to be a space separated CSV file, with each row consisting of the URI of the source element, a space, and then the URI of the target element.

Configure the [`manual_evaluation.py`](https://github.com/paolo7/prohow-links-manual-evaluator/blob/master/manual_evaluation.py) script to point to the right folders and the links file. A shuffled version of the links file will be created and used in the evaluation. This ensures that the links are evaluated in a random order. The shuffling code used is in the [`shuffle_all.py`](https://github.com/paolo7/prohow-links-manual-evaluator/blob/master/shuffle_all.py) script.

Run the script [`manual_evaluation.py`](https://github.com/paolo7/prohow-links-manual-evaluator/blob/master/manual_evaluation.py) and annotate each link with the letters:
 - `p` if the link is correct
 - `q` if the link is wrong
 - `s` to skip the link if the link should not be counted
 - `e` when the evaluation should terminate
  
The manual evaluation can be interrupted and resumed at any time without losing the previously done annotations.
The statistics of the evaluation will be saved in a file called `r_log.csv`. The correct links will be stored in the `r_pos.csv` file, the negative in `r_neg.csv` and the skipped in `r_skipped.csv`.

