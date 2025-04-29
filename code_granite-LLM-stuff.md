git clone https://github.com/ibm-granite/dolomite-engine/
cd dolomite-engine

# you might need to modify configs/granite-example/training.yml
sh scripts/finetune.sh configs/granite-example/training.yml

# once the model is trained, convert to HuggingFace-compatible safetensors
sh scripts/export.sh configs/granite-example/export.yml


^^^^^^ REQUIRES an email into the Git Resource to pull ^^^^^^^^^^^


git clone https://huggingface.co/ibm-granite/granite-3b-code-base-2k


git clone https://huggingface.co/ibm-granite/granite-3b-code-base-2k
git clone https://huggingface.co/ibm-granite/granite-3b-code-instruct-2k
git clone https://huggingface.co/ibm-granite/granite-8b-code-base-4k
git clone https://huggingface.co/ibm-granite/granite-8b-code-instruct-4k
git clone https://huggingface.co/ibm-granite/granite-20b-code-base-8k
git clone https://huggingface.co/ibm-granite/granite-20b-code-instruct-8k
git clone https://huggingface.co/ibm-granite/granite-34b-code-base-8k
git clone https://huggingface.co/ibm-granite/granite-34b-code-instruct-8k


(pi6U3a?@IXVVctqgb5jC0=%VPCV9UDQ --- PO