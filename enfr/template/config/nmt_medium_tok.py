import tensorflow as tf
import opennmt as onmt

def model():
    return onmt.models.SequenceToSequence(
        source_inputter=onmt.inputters.WordEmbedder(
            vocabulary_file_key="source_words_vocabulary",
            embedding_size=512, 
            tokenizer=onmt.tokenizers.OpenNMTTokenizer(
                configuration_file_or_key="source_tokenizer_config")),
        target_inputter=onmt.inputters.WordEmbedder(
            vocabulary_file_key="target_words_vocabulary",
            embedding_size=512, 
            tokenizer=onmt.tokenizers.OpenNMTTokenizer(
                configuration_file_or_key="target_tokenizer_config")),
        encoder=onmt.encoders.BidirectionalRNNEncoder(
            num_layers=4,
            num_units=512,
            reducer=onmt.layers.ConcatReducer(),
            cell_class=tf.contrib.rnn.LSTMCell,
            dropout=0.3,
            residual_connections=False),
        decoder=onmt.decoders.AttentionalRNNDecoder(
            num_layers=4,
            num_units=512,
            bridge=onmt.layers.CopyBridge(),
            attention_mechanism_class=tf.contrib.seq2seq.LuongAttention,
            cell_class=tf.contrib.rnn.LSTMCell,
            dropout=0.3,
            residual_connections=False)
    )
