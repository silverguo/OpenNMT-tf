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
segment text into subword units by python package
```bash
subword-nmt learn-joint-bpe-and-vocab --input {train_file}.L1 {train_file}.L2 -s {num_operations} -o {codes_file} --write-vocabulary {vocab_file}.L1 {vocab_file}.L2
```
re-apply with vocab filter
```bash
subword-nmt apply-bpe -c {codes_file} --vocabulary {vocab_file}.L1 --vocabulary-threshold 50 < {train_file}.L1 > {train_file}.BPE.L1
```

## build vocabulary
build vocab with bpe tok
```bash
onmt-build-vocab --tokenizer OpenNMTTokenizer --tokenizer_config token_config --size 50000 --save_vocab vocab_path train_path
```

## train
```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 onmt-main train_and_eval --model model_path --config train_config --num_gpus 4
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


