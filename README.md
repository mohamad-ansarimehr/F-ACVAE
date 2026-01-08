# F-ACVAE: Federated Adaptive Conditional Variational Auto-Encoder for Privacy-Preserving Intrusion Detection in IoT Networks

**F-ACVAE** is a privacy-preserving federated learning framework that extends the centralized **Conditional Variational Auto-Encoder (CTVAE)** paradigm to highly heterogeneous IoT environments.  
The proposed approach is specifically designed to address extreme non-IID data distributions while preserving data privacy and minimizing communication overhead.

## Key Features
- **Strict raw data privacy**: No raw data is exchanged between clients and the server during training.
- **Selective parameter aggregation**:  
  Only a subset of model parameters, including class-conditioned latent priors and decoder-related components, are aggregated, while local encoders remain private at the client side.
- **Constrained Momentum Gaussian Aggregation (CMGA)**:
  - Momentum-based aggregation for stabilizing class-specific Gaussian priors  
  - Constraint-aware updates to preserve inter-class separability in the latent space  
  - Robust performance under severe non-IID and device-heterogeneous settings
- **Superior performance compared to centralized baselines**:
  - Achieves the highest accuracy in **8 out of 9 device-specific subsets**
  - Best overall **average accuracy of 99.0%**
  - Consistently superior **Macro F1-score across all scenarios**, with an average value of **99.0%**

## Dataset
The proposed framework is evaluated on the benchmark **N-BaIoT** dataset, using nine device-specific subsets that simulate realistic IoT botnet traffic scenarios, including **Mirai** and **Bashlite** attacks, under highly heterogeneous and non-IID conditions.

## Implementation
- Implemented using **PyTorch** and the **Flower (flwr)** federated learning framework
- Custom federated strategy for selective parameter aggregation and CMGA-based updates
- End-to-end pipeline including server initialization, client-side training, and inference

## Results
Experimental results demonstrate that F-ACVAE consistently outperforms the centralized CTVAE baseline across most device-specific subsets, despite operating in a federated and privacy-preserving setting.  
The results highlight the effectiveness of the proposed aggregation strategy in maintaining a well-conditioned and discriminative latent representation without raw data exchange.

## Paper
**F-ACVAE: A Federated Adaptive Conditional VAE for Privacy-Preserving Intrusion Detection in IoT Networks**  
Mohammad Ansarimehr, Somayeh Changiz, Ehsan Baghshani, Ali Mousavi

## Repository Contents
- Source code for model architecture, federated training, and evaluation
- Scripts for reproducing experiments on the N-BaIoT dataset
- Configuration files and trained model checkpoints

## Citation
If you use this method or code in your research, please cite:

```bibtex
@article{ansarimehr2025facvae,
  title={F-ACVAE: A Federated Adaptive Conditional Variational Auto-Encoder for Privacy-Preserving Intrusion Detection in IoT Networks},
  author={Ansarimehr, Mohammad and Changiz, Somayeh and Baghshani, Ehsan and Mousavi, Ali},
  journal={IEEE Transactions on ...}, % To be updated
  year={2025}
}
