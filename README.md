nlp-augment
===========
A collection of utilities used in exploring data augmentation of low-resource
parallel corpuses.

## Example usage

### Create word embeddings

    $ word2vec/bin/./word2vec -train ug.mono -output ug.bin -size 100 -sample 1e-5 -negative 5 -threads 8 -binary 1

### Collect rare words

    $ python build-rare.py --data_in train.src --rare_out 1k.train.src.rare --rare_num 1000
    $ python build-rare.py --data_in train.trg --rare_out 1k.train.trg.rare --rare_num 1000

My experiments suggest that augmenting _only_ the source side of the parallel 
data with rare words is more beneficial.

### Find similar non-common words

    $ ./distance-list ug.bin train.src.rare > train.src.rare.sim 2>/dev/null
    $ python clean-sim.py --sim_in train.src.rare.sim --sim_out train.src.rare.clean.sim --mono ug.mono

### Generate new sentence augmentations
```
$ python augment.py --data_src train.src --data_trg train.trg \
    --rare_src train.src.rare --rare_trg train.trg.rare \
    --sim_src train.src.rare.clean.sim --sim_trg train.trg.rare.clean.sim \
    --out_src train.src.aug --out_trg train.trg.aug
```

## Author's experiment
Training the [ZophRNN](https://github.com/isi-nlp/Zoph_RNN) framework on
in-house Uyghur to English data, I raise the word count (`wc -w`) from 3M to
15M words.

| Model | dev | test1 | test2 | test3 |
| ----- | --- | ----- | ----- | ----- |
| baseline | 10.8 | 11.6 | 10.1 | 4.0 |
| augmented| 12.8 | 10.6 | 10.4 | 4.4 |
