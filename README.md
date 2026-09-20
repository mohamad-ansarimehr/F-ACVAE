# F-ACVAE — Final Reproducible Project

This folder contains three aligned outputs derived from the final version of the paper code:

```text
F_ACVAE.py              # Standalone single-file Python implementation
F_ACVAE_clean.ipynb     # Clean and executable project notebook
README.md				# English project structure and execution documentation
README (fa).md 			# Farsi project structure and execution documentation
```

## Project Overview

**F-ACVAE** is a federated adaptive conditional variational autoencoder for intrusion detection in heterogeneous Internet of Things (IoT) traffic. It combines client-local representation learning, selectively shared decoder and class-conditioning parameters, and server-coordinated class-wise Gaussian priors. The design addresses non-IID client data while avoiding direct transfer of clients’ raw training data. Its complete algorithm-to-code mapping appears in the [Paper-to-Code Guide](#paper-to-code-guide-algorithms-and-methodology).

### Key Features

- **Data locality:** Clients train on their own traffic; raw input records are not included in the model-update exchange. This architecture reduces direct data exposure but is **not** a formal differential-privacy guarantee.
- **Selective communication:** Private encoder parameters remain client-local in the communicated model state. Shared decoder and class-conditioning parameters, together with class-wise Gaussian summary statistics, are coordinated by the server.
- **CMGA with MSA:** CMGA coordinates shared parameters and class priors; its MSA subroutine clamps, sample-weights, and momentum-smooths **model updates**. Class-prior smoothing and separation are distinct CMGA operations.
- **Client-local intrusion classification:** Each client evaluates a Random Forest on latent features from its private encoder; other classifiers in the code are supplementary experiments.

### Datasets and Reported Paper Results

The paper evaluates **11 N-BaIoT scenarios** involving traffic from the **Mirai** and **Bashlite (Gafgyt)** botnets, and reports additional experiments on **UNSW-NB15** and **CIC-IDS2017**. The *revised manuscript* reports **97.3% average accuracy** and **93.4% average macro F1** across the 11 N-BaIoT scenarios, alongside approximately **50% lower model-communication volume** through selective sharing. These are **reported manuscript results**, not measurements produced by merely starting this code; individual scenarios and evaluation protocols can have different outcomes. See the [Datasets](#datasets) and [Reproducibility](#reproducibility) sections for execution requirements.

**Implementation distinction:** The manuscript discusses Flower-based orchestration; this distributed workflow is implemented **within one Python process** in the supplied standalone `F_ACVAE.py`. The script does not launch Flower clients or a Flower server, and its experiment checkpoints can contain full local model states to support resuming runs. See Algorithm 1 and the privacy note in the guide below.

## Quick Start — Python Version

`F_ACVAE.py` is a standalone script and does not depend on any additional Python source files for the project logic. Place it in the project directory and put the datasets either next to it or inside one of the supported folders: `dataset/`, `datasets/`, or `data/`.

```powershell
python .\F_ACVAE.py
```

On Windows, you can also use the Python Launcher:

```powershell
py .\F_ACVAE.py
```

## Automatic Dependency Installation

At startup, the script checks whether the required packages can be imported. Only missing or broken dependencies are installed automatically through `pip` using the same active Python interpreter.

The main dependencies are NumPy, pandas, Matplotlib, scikit-learn, PyTorch, and IPython. `PyArrow` is checked only when Parquet input is actually required and is installed automatically if missing.

If a working PyTorch installation already exists, it is preserved. This avoids unnecessarily replacing an existing CUDA/GPU-compatible environment. Internet access is required only when a missing dependency needs to be installed.

## Recommended Project Structure

Simple layout — datasets directly next to the code:

```text
F_ACVAE_Project/
├── F_ACVAE.py
├── F_ACVAE_clean.ipynb
├── README.md
├── README (fa).md
├── N-BaIoT/
├── UNSW-NB15/
└── CIC-IDS2017/
```

Alternatively:

```text
F_ACVAE_Project/
├── F_ACVAE.py
├── F_ACVAE_clean.ipynb
├── README.md
├── README (fa).md
└── dataset/
    ├── N-BaIoT/
    ├── UNSW-NB15/
    └── CIC-IDS2017/
```

The folder names `data/` and `datasets/` are also supported instead of `dataset/`.

## Datasets

The default full run includes the N-BaIoT outputs and Table VII. Therefore, all three datasets below are required for the complete execution:

- `N-BaIoT`
- `UNSW-NB15`
- `CIC-IDS2017`

For N-BaIoT, the code recognizes common device-directory names and typical attack-file layouts. For UNSW-NB15, processed CSV files are supported. For CIC-IDS2017, both CSV and Parquet inputs are supported. When Parquet files are used, `pyarrow` is installed automatically if required.

If N-BaIoT is stored in a separate location, its path can be set explicitly:

```powershell
$env:N_BAIOT_ROOT="D:\Datasets\N-BaIoT"
python .\F_ACVAE.py
```

## Running Only Selected Outputs

The Python version allows you to select specific outputs without editing the source file. For example:

```powershell
$env:FACVAE_OUTPUTS="TABLE_VI,FIGURE_3,FIGURE_4"
python .\F_ACVAE.py
```

If `TABLE_VII` is not selected, the external datasets required for that experiment are not needed for the run.

## Clean Notebook

`F_ACVAE_clean.ipynb` was created from the final paper notebook with the following execution-oriented cleanup:

- Previous cell outputs and `execution_count` values were removed.
- Repetitive Markdown content was shortened and section structure was clarified.
- Unnecessary side explanations were reduced.
- A setup cell was added to install missing dependencies automatically.
- Dataset discovery now checks the project directory as well as `dataset/`, `datasets/`, and `data/`.
- A pre-flight check verifies that the datasets required by the selected outputs are available before expensive execution begins.
- The core computational logic for the model, training, evaluation, and paper outputs was preserved.

For the notebook version, it is recommended to open VS Code/Jupyter from the project directory and execute the cells from top to bottom. If needed, the project root can be set explicitly through `FACVAE_PROJECT_ROOT`.

## Outputs and Checkpoints

The main paper outputs are stored under the `Results/` structure. Existing checkpoints and caches can be reused to avoid repeating expensive computations. Runtime log files are also created locally within the project structure.

## Reproducibility

The main parameters from the final paper implementation—including seeds, number of clients, model configuration, data splits, classifiers, and checkpoint logic—were preserved from the final notebook.

The changes made in this package are limited to execution portability, path handling, dependency installation, and documentation cleanup. They do not alter the scientific method or intentionally modify the reported results.

The binary open-set details remain available in the source code. To keep this README concise, that part is not expanded here.

## Paper-to-Code Guide: Algorithms and Methodology

This section follows the **order and terminology of the accompanying revised manuscript** (`Revised (6.2 - Integration).tex`). The paper's algorithm titles are retained verbatim; Python names below refer to the actual symbols in [`F_ACVAE.py`](F_ACVAE.py). A *paper algorithm* is sometimes implemented across several Python methods rather than in a single identically named function.

### Algorithm 1 — Flower-Based Federated Learning Server

**Paper location:** Background → *Flower Federated Learning Framework*; Algorithm `alg:flower-base`.

**Purpose and workflow.** This algorithm describes the federated coordination loop: initialize the global model, select participating clients, distribute the current shared parameters and configuration, perform local training, collect client updates and sample counts, aggregate updates, and evaluate the resulting model. The manuscript's experimental protocol uses **all nine clients in every round**, rather than subsampling a smaller group.

**Corresponding implementation:**

| Python symbol | Role in the workflow |
| --- | --- |
| `FederatedServer.__init__()` | Initializes global communicated parameters and, when needed, CMGA momentum and class-prior state. |
| `FederatedServer.add_client()` | Registers each compatible client and initializes its communicated model state. |
| `FederatedServer.train_round()` | Performs one round: invokes client training, builds sample-count weights, aggregates updates, updates priors, and distributes the new shared state. |
| `FederatedClient.train_local()` | Implements the client-side work requested during a round. |
| `run_method()` | Builds a server and clients, iterates over communication rounds, records validation measurements, and saves/restores checkpoints. |
| `FederatedServer.communication_accounting()` | Reports the number of communicated model parameters and Gaussian-statistic values. |

**Inputs:** Client data records, method specification (`MethodSpec`), and experimental settings (`ProtocolConfig`). **Outputs:** Updated shared state, optional coordinated class priors, and per-round training/evaluation records. For the main nine-client experiment, `ProtocolConfig` sets `num_clients=9` and `rounds=10`.

**Implementation boundary:** The manuscript describes a *Flower-based* server, but this particular standalone `.py` file implements its coordinator **in process**, using Python objects and a sequential client loop in `FederatedServer.train_round()`; it does not import or start the Flower runtime. It represents the paper's coordination logic for reproducible local experiments, not a networked multi-device deployment. `run_method()` also handles checkpointing, which is an execution facility rather than a step of Algorithm 1.

### Algorithm 2 — Adaptive Conditional Latent Generation (ACVAE)

**Paper location:** Proposed Methodology → *Adaptive Conditional VAE Architecture (ACVAE)*; Algorithm `alg:acvae`.

**Purpose and workflow.** Given a feature vector `x` and a class label `y`, the local encoder estimates the mean and log variance of a diagonal Gaussian posterior. The model samples a latent vector through reparameterization and adds a learned class embedding to it:

```text
(mu, logvar) = encoder(x)
z = mu + exp(0.5 * logvar) * epsilon, epsilon ~ N(0, I)
z_cond = z + condition_scale * class_embedding(y)
x_hat = decoder(z_cond)
```

`condition_scale` corresponds to the manuscript's conditioning coefficient `λ_c`. The conditioned latent is used for **training-time reconstruction**. At classifier evaluation, the implementation instead extracts the *unconditioned encoder mean* `mu(x)` without supplying a true class label.

**Corresponding implementation:**

| Python symbol | Role in the workflow |
| --- | --- |
| `FederatedVAE.__init__()` | Creates the private `encoder`, shared `decoder`, and optional class-embedding layer `mapper`. |
| `FederatedVAE.encode()` | Produces posterior `mu` and clamped `logvar` from the feature vector. |
| `FederatedVAE.reparameterize()` | Samples the latent code using Gaussian noise and the posterior parameters. |
| `FederatedVAE.training_forward()` | Applies additive class conditioning and reconstructs the input. |
| `FederatedVAE.parameter_partition()` | Identifies private `encoder.*` parameters and shared `mapper.*`/`decoder.*` parameters. |
| `FederatedVAE.communicated_state_dict()` / `FederatedVAE.load_communicated_state_dict()` | Exports and loads the parameter subset declared by the method's selective-communication setting. |
| `FederatedClient.extract_mu()` | Produces label-free encoder-mean representations for downstream evaluation. |

**Inputs:** A batch `(x, y)`, feature/class dimensions, and conditioning scale. **Outputs:** Posterior parameters, sampled and conditioned latent codes, and reconstruction; `extract_mu()` separately returns the inference-time latent mean and aligned labels/inputs for evaluation.

### Algorithm 3 — Constrained Momentum Gaussian Aggregation (CMGA)

**Paper location:** Proposed Methodology → *Constrained Momentum Gaussian Aggregation (CMGA)*; Algorithm `alg:flower-cmga`.

**Purpose and workflow.** CMGA is the **complete server-side coordination strategy**. In each round, the server receives (1) client updates for the communicated model subset, (2) training-sample counts, and (3) per-class Gaussian latent statistics. It validates and aggregates shared updates through the **MSA subroutine** described below, then pools the Gaussian statistics into class-wise global priors. Priors are temporally smoothed, class means undergo a proximity-constrained separation adjustment, and prior variances are lower-bounded before the next round.

**Corresponding implementation:**

| Python symbol | Role in the workflow |
| --- | --- |
| `MethodSpec` / `METHOD_SPECS` | Select the full proposed `F_ACVAE_CMGA` variant and its selective communication, conditioning, and coordinated-prior behavior. |
| `FederatedClient.train_local()` | Returns a `shared_update`, local `samples` count, and the optional `gaussian` statistics. |
| `FederatedClient.compute_class_gaussian_statistics()` | Computes per-class count, mean, and variance from the client's training-set encoder means. |
| `FederatedServer.train_round()` | Coordinates local results, calls shared-update aggregation, refreshes global priors, and loads updated shared parameters into clients. |
| `_aggregate_model_state()` | Performs the shared-parameter update, including the MSA steps when aggregation is `CMGA`. |
| `_pool_class_gaussians()` | Combines client class counts, means, and variances into pooled class-wise Gaussian statistics. |
| `FederatedServer._update_cmga_priors()` | Smooths observed class means/variances, adjusts means, and enforces minimum variance. |
| `_proximal_prior_separation()` | Refines class-prior means using a proximity term and a pairwise-separation penalty. |

**Inputs:** Previous global shared state, momentum buffer and class priors, plus the current round's per-client results. **Outputs:** New shared state, updated momentum buffer and coordinated class-wise Gaussian priors. The relevant configuration fields are `cmga_prior_beta`, `cmga_prior_margin`, `cmga_prior_penalty`, `cmga_prior_pgd_steps`, `cmga_prior_pgd_lr`, and `cmga_min_prior_variance` in `ProtocolConfig`.

**Distinction from MSA:** CMGA owns *both* shared-parameter coordination and Gaussian-prior coordination. MSA is only the shared-parameter stabilization step inside `_aggregate_model_state()`; prior pooling and constrained mean adjustment are separate server operations.

### Algorithm 4 — Local Client Optimization Procedure

**Paper location:** Proposed Methodology → *Local Training and Objective Function*; Algorithm `alg:client`.

**Purpose and workflow.** A client receives the latest communicated parameters and, for the proposed CMGA variant, the coordinated class priors. It loads **only the communicated model state**, preserving its private encoder in the selective variant. For each local batch, it generates the conditioned latent representation, reconstructs the input, evaluates reconstruction plus KL loss, backpropagates, clips the gradient norm, and performs an AdamW optimizer step. After its local epochs, it returns the difference between the new and received communicated parameter values, together with per-class latent statistics for CMGA.

The manuscript defines the local objective as reconstruction MSE plus `β × KL(q(z|x) || p_y(z))`. In the code, `FederatedVAE.loss_terms()` uses the class-conditioned coordinated prior when `prior_mu` and `prior_var` are supplied; otherwise it uses the standard normal prior for the relevant baseline/ablation. The code also implements a **FedProx-specific** proximal term, but only when the method specification requests that comparison baseline.

**Corresponding implementation:**

| Python symbol | Role in the workflow |
| --- | --- |
| `FederatedClient._loader()` | Creates deterministic local mini-batches from a selected split. |
| `FederatedClient.train_local()` | Loads communicated parameters; runs AdamW local epochs, loss/gradient processing, and returns the update plus statistics. |
| `FederatedVAE.training_forward()` | Encodes, conditions, and reconstructs each training batch. |
| `FederatedVAE.loss_terms()` | Calculates reconstruction MSE, KL divergence, and the total VAE loss. |
| `FederatedVAE.communicated_state_dict()` | Captures the communicated state before and after local training to form the transmitted delta. |
| `FederatedClient.compute_class_gaussian_statistics()` | Builds the sufficient statistics sent by a CMGA client after optimization. |
| `ProtocolConfig` | Holds `local_epochs`, `batch_size`, `local_lr`, `weight_decay`, `kl_weight`, and `gradient_clip_norm`. |

**Inputs:** One client's training data, current shared parameter state, local optimizer settings, and optional CMGA priors. **Outputs:** Per-round client update, training-sample count, optional Gaussian statistics, and local loss diagnostics. Gradient-*norm* clipping (`gradient_clip_norm=0.5`) here is distinct from the server-side *element-wise update* clamp in MSA.

### Momentum-Stabilized Aggregation (MSA) — Subroutine of Algorithm 3

**Paper location:** Proposed Methodology → *Momentum-Stabilized Aggregation (MSA)*; the manuscript presents this as a named subroutine, **not a separate numbered algorithm**.

**Purpose and workflow.** MSA stabilizes the communicated-model update: element-wise clamp each client's parameter delta, combine deltas using sample-count weights, smooth the aggregate with the previous momentum buffer, and apply a scaled global step.

```text
clamped_delta[k] = clamp(delta[k], -tau_clamp, +tau_clamp)
mean_delta = sum_k((n_k / sum_j n_j) * clamped_delta[k])
velocity = gamma * mean_delta + (1 - gamma) * previous_velocity
new_global_state = previous_global_state + alpha * velocity
```

**Corresponding implementation:** `_aggregate_model_state()` contains the clamp, sample-weighted mean, persistent velocity update, and global step in its `CMGA` branch; `FederatedServer.train_round()` supplies the sample-count weights and stores the resulting velocity. `FederatedServer.__init__()` initializes the velocity buffer. `ProtocolConfig` sets `cmga_alpha=0.1`, `cmga_gamma=0.1`, and `cmga_update_clip_abs=0.2`.

**Inputs:** Current communicated state, client deltas, normalized sample-count weights, previous velocity, and MSA hyperparameters. **Outputs:** Updated shared state, updated velocity, and aggregation diagnostics. This part **does not** compute, pool, or separate Gaussian class priors; those are CMGA operations described in Algorithm 3.

### Hybrid Latent Feature Classification

**Paper location:** Proposed Methodology → *Hybrid Latent Feature Classification*; this is a methodology subsection rather than a numbered pseudocode algorithm.

**Purpose and workflow.** Following federated representation learning, each client computes `z = mu(x)` with its **private encoder** and trains a **client-specific Random Forest** in that client's latent space. The final held-out test procedure fits each classifier on that client's **train and validation** latent representations, then evaluates it on the corresponding client test split. Client predictions are combined through confusion matrices and reported as accuracy, macro F1, and related metrics; no common pooled classifier is substituted for the primary client-local RF protocol.

**Corresponding implementation:**

| Python symbol | Role in the workflow |
| --- | --- |
| `FederatedClient.extract_mu()` | Extracts latent means without passing labels to the encoder. |
| `_client_split_arrays()` | Collects aligned latent vectors and labels for the requested client split(s). |
| `_make_classifier("rf", ...)` / `RF_PARAMS` | Builds the paper's RF configuration: 100 trees, maximum depth 15, minimum split 10, minimum leaf 5, and `sqrt` features. |
| `evaluate_client_local_classifier()` | Fits/evaluates one classifier per client and aggregates confusion matrices; the later definition in the file is the effective implementation and handles single-class local training splits without dropping clients. |
| `run_method()` | Computes the training-only-fit **validation** RF result for each model variant. |
| `run_final_test_once()` | Computes the **final test** local RF with `("train", "validation")` as the classifier training splits, while also reporting separately identified diagnostics. |
| `_metrics_from_confusion()` | Calculates aggregate classification measurements from the collected confusion matrix. |

**Inputs:** Trained client encoders, each client's train/validation/test records, and RF settings. **Outputs:** Client-specific predictions and aggregated classification metrics. Other classifiers and cross-client evaluations in the script are additional analyses, not replacements for the paper's primary client-local RF.

### Supporting Pipeline and Paper Outputs

The following stages make the algorithms reproducible but are **not additional numbered algorithms in the manuscript**.

| Paper section / stage | Corresponding Python symbols | Purpose |
| --- | --- | --- |
| Experimental Settings → Datasets and Evaluation Protocol | `build_iot01_data()`, `build_nbaiot_scenario_data()`, `build_cross_dataset_bundle()` | Prepare N-BaIoT scenarios and the UNSW-NB15/CIC-IDS2017 cross-dataset experiments. |
| Leakage-aware splitting and preprocessing | `_build_raw_splits()`, `_fit_transformer()`, `_transform_shared()`, `_sample_partition_proportions()`, `_partition_indices()` | Construct splits, fit the feature transformer on training data, and maintain the non-IID client-partition protocol. |
| Experimental Settings → Parameter Settings | `ProtocolConfig`, `PipelineConfig`, `RF_PARAMS`, `reset_all_seeds()` | Define the training, partition, classifier, and reproducibility settings. |
| Results → Performance and ablations | `METHOD_SPECS`, `PAPER_ABLATION_SPECS`, `run_method()`, `run_final_test_once()` | Keep proposed/baseline/ablation variants distinct and execute the paper evaluations. |
| Results → Communication efficiency | `FederatedServer.communication_accounting()` | Account for communicated trainable parameters and Gaussian-statistic values. |
| Experiment persistence | `_save_round_checkpoint()`, `_restore_latest_checkpoint()` | Save and resume training without changing the mathematical method. |

**Scope and privacy note:** The selective-aggregation rule excludes private encoder parameters from the **communicated model update**. In this single-process research runner, however, the server and client objects coexist in one Python process and experiment checkpoints contain full client model states to support resumption. This is not equivalent to deploying independent clients with protected on-device storage, nor does the manuscript claim formal differential privacy.

## Validation Performed on This Release

- `F_ACVAE.py` was checked for Python syntax using `py_compile`.
- The Python version does not require local imports from additional project `.py` files.
- All code cells in `F_ACVAE_clean.ipynb` were compiled individually.
- The notebook structure was validated with `nbformat`.

A complete end-to-end training run was not performed at this stage because it requires the full large-scale datasets and the corresponding training time. Therefore, the performed validation is structural and syntactic rather than a complete reproduction of every reported experimental result.

## Manuscript and Citation

**Title:** *F-ACVAE: A Federated Adaptive Conditional Variational Auto-Encoder for Privacy-Preserving Intrusion Detection in IoT Networks*  
**Authors (as listed in the supplied revised manuscript):** Mohammad Ansarimehr, Samira Sarvin, Ehsan Baghishani, Ali Mousavi.

A provisional, publication-neutral BibTeX entry is provided below. **Confirm the final author list, publication venue, year, volume, pages, and DOI against the published article before using this citation in a paper.**

```bibtex
@unpublished{ansarimehr_facvae,
  title  = {F-ACVAE: A Federated Adaptive Conditional Variational Auto-Encoder for Privacy-Preserving Intrusion Detection in IoT Networks},
  author = {Ansarimehr, Mohammad and Sarvin, Samira and Baghishani, Ehsan and Mousavi, Ali},
  note   = {Revised manuscript; update publication metadata when available}
}
```

The supplied manuscript identifies its source-code repository as <https://github.com/mohamad-ansarimehr/F-ACVAE> and references a software archive at <https://doi.org/10.5281/zenodo.17919997>. These links are reproduced from that manuscript; this README does not claim to have independently verified their current status or content.
