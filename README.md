# Raccoon
**Raccoon**  is a test bench for prompt extraction attacks on LLM-Integrated Applications. With the proliferation of LLM-integrated applications such as GPT-s, millions are deployed, offering valuable services through proprietary instruction prompts. These systems, however, are prone to prompt extraction attacks through meticulously designed queries. To help mitigate this problem, we introduce the **Raccoon** benchmark which comprehensively evaluates a model's susceptibility to prompt extraction attacks. 

![Raccoon](figures/raccoon.png)

We evaluate systems 

- Under both defenseless and defended scenarios, employing a dual approach to evaluate the effectiveness of existing defenses and the resilience of the models. 
- The benchmark encompasses 14 categories of prompt extraction attacks, with additional compounded attacks that closely mimic the strategies of potential attackers.
- A diverse collection of defense templates. This array is, to our knowledge, the most extensive compilation of prompt theft attacks and defense mechanisms to date. 

![Raccoon](figures/model_susceptibility_max.png)



## News and Updates

- [05/24/2024] Publish initial release of Raccoon (GPTs data will be released soon)
- [05/17/2024] Our paper has been accepted by ACL 2024 Findings

## Table of Contents

- [Raccoon](#raccoon)
  - [News and Updates](#news-and-updates)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
      - [1. Run benchmark on Singular attacks, Defenseless GPTs, GPT-3.5-0125](#1-run-benchmark-on-singular-attacks-defenseless-gpts-gpt-35-0125)
      - [2. Run benchmark on Top 5 Singular attacks, Defended GPTs, GPT-3.5-0125](#2-run-benchmark-on-top-5-singular-attacks-defended-gpts-gpt-35-0125)
      - [3. Run benchmark on Compound attacks, Defenseless GPTs, GPT-3.5-0125](#3-run-benchmark-on-compound-attacks-defenseless-gpts-gpt-35-0125)
      - [4. Run benchmark on Compound attacks, Defended GPTs, GPT-3.5-0125](#4-run-benchmark-on-compound-attacks-defended-gpts-gpt-35-0125)
  - [Components](#components)

## Installation

> ```bash
> $ conda create --name <env> --file requirements.txt
> ```

## Usage

#### 1. Run benchmark on Singular attacks, Defenseless GPTs, GPT-3.5-0125

```shell
python run_raccoon_gang.py \
--model_name gpt-3.5-0125 \
--gpts_path "./Data/gpts/gpts196" \
--attack_path "./Data/attacks/singular_attacks" \
--ref_def_path "./Data/reference/gpts196_defense_prompt.json" \
--def_tmpl_path "./Data/defenses/defense_template.json" \
--use_sys_template \
--use_defenseless_user_prompt
```

#### 2. Run benchmark on Top 5 Singular attacks, Defended GPTs, GPT-3.5-0125

```shell
python run_raccoon_gang.py \
--model_name gpt-3.5-0125 \
--gpts_path "./Data/gpts/gpts196" \
--attack_path "./Data/attacks/singular_attacks_deflesstop5" \
--ref_def_path "./Data/reference/gpts196_defense_prompt.json" \
--def_tmpl_path "./Data/defenses/defense_template.json" \
--use_sys_template \
--use_custom_defenses
```

#### 3. Run benchmark on Compound attacks, Defenseless GPTs, GPT-3.5-0125

```shell
python run_raccoon_gang.py \
--model_name gpt-3.5-0125 \
--gpts_path "./Data/gpts/gpts196" \
--attack_path "./Data/attacks/compound_attacks" \
--ref_def_path "./Data/reference/gpts196_defense_prompt.json" \
--def_tmpl_path "./Data/defenses/defense_template.json" \
--use_sys_template \
--use_defenseless_user_prompt
```

#### 4. Run benchmark on Compound attacks, Defended GPTs, GPT-3.5-0125

```shell
python run_raccoon_gang.py \
--model_name gpt-3.5-0125 \
--gpts_path "./Data/gpts/gpts196" \
--attack_path "./Data/attacks/compound_attacks" \
--ref_def_path "./Data/reference/gpts196_defense_prompt.json" \
--def_tmpl_path "./Data/defenses/defense_template.json" \
--use_sys_template \
--use_custom_defenses
```

## Components

- **Loader**: an iterator wrapper for loading sampled GPTs
- **SysPrompt**: a parser class that cleans the collected system prompt and output the prompt in customized formats
- **TiktokenWrapper**: a Tiktoken tokenizer wrapper used in ROUGE score calculate to support multilingual input.
- **Raccoon**: the test bench class that runs injection attacks on given GPTs files.

## Attack Categories

![Raccoon](figures/Attack_Categories.png)

## Citation