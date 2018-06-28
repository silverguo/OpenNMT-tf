# enfr

## processed
- europarl
- Tatoeba 
- JRC-Acquis
- newstest (dev 2015)

## to clean
- common crawl
- undoc
- giga

### to download
- GlobalVoices
- TedTalk
- EAC
- Multi30k
- [OPUS](http://opus.nlpl.eu/)

## data clean
```bash
# TBD
```

## normalization
some uniform transformation on the source sequences to identify and protect some specific sequences (for instance url), normalize characters (for instance all types of quotes, unicode variants) or even to normalize some variants (like dates) into unique representation simpler for the translation process
```bash
# TBD
```

## tokenization before bpe
```bash
onmt-tokenize-text --tokenizer OpenNMTTokenizer --tokenizer_config enfr/config/tokenization/no_bpe.yml < input > output
```

## bpe
segment text into subword units
```bash
th tools/learn_bpe.lua -tok_mode aggressive -tok_segment_numbers -tok_case_feature -size 32000 -save_bpe /path/to/bpe < /path/to/input
```

## tokenization
transform the sentence into a sequence of space-separated tokens together with possible features
```bash
th tools/tokenize.lua -mode aggressive -segment_numbers -case_feature -joiner_annotate -nparallel 20 -bpe_model /path/to/bpe < /path/to/input > /path/to/input_tok
```

## preprocess
```bash
th preprocess.lua -train_src /train/src -train_tgt /train/tgt -valid_src /valid/src -valid_tgt /valid/tgt -save_data /save/data -src_vocab_size 50000
```

## train
```bash
th train.lua -layers 4 -word_vec_size 800 -encoder_type brnn -residual -rnn_size 800 -start_decay_at 6 -end_epoch 20 -gpuid 1 -data /load/data -save_model /save/model -log_file /save/log
```

## release
```bash
th tools/release_model.lua -gpuid 1 -model /path/model
```

## translate
```bash
th translate.lua -replace_unk -tok_src_mode aggressive -tok_tgt_mode aggressive -tok_src_case_feature -tok_tgt_case_feature -tok_src_segment_numbers -tok_tgt_segment_numbers -tok_src_joiner_annotate -tok_tgt_joiner_annotate -detokenize_output -beam_size 10 -tok_src_bpe_model /src/bpe -tok_tgt_bpe_model /tgt/bpe -model /path/model -src /path/src -output /path/output
```

## server
```bash
th tools/rest_translation_server.lua -host 127.0.0.1 -port 9201 -mode aggressive -segment_numbers -joiner_annotate -replace_unk -beam_size 10 -case_feature -bpe_model /path/bpe -model /path/model 
```

## multi server
```bash
th tools/rest_multi_models.lua -port 9201 -model_config /path/yml
```
config file example
```yaml
-
  model: '/path/model'
  mode: 'aggressive'
  case_feature: true
  segment_numbers: true
  bpe_model: '/model/bpe'
  joiner_annotate: true
  replace_unk: true
  beam_size: 10
```


