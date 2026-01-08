# Constrained Momentum Gaussian Aggregation (CMGA)

**Constrained Momentum Gaussian Aggregation (CMGA)** is a custom server-side aggregation strategy proposed for the federated **Adaptive Conditional Variational Auto-Encoder (F-ACVAE)** framework.  
CMGA is implemented as a custom **Flower (flwr)** strategy and replaces conventional FedAvg to address the destructive effects of naive parameter averaging on class-conditioned latent representations under severe non-IID data distributions.

By enabling selective aggregation, stabilizing class-specific Gaussian priors, and explicitly enforcing inter-class separation in the latent space, CMGA plays a key role in achieving superior detection performance while preserving strict raw-data privacy.

## Core Mechanisms

### 1. Selective Parameter Aggregation
Only globally beneficial components are shared and aggregated:
- Shared latent mapper
- Decoder
- Class-conditioned Gaussian prior parameters: `{μ_c, log σ²_c}` for each class `c = 1, ..., C`

**Local encoders** remain strictly private on each client and are never transmitted.

**Benefit**: Significantly reduces communication overhead while preventing leakage of client-specific feature representations.

### 2. Momentum-Enhanced Aggregation of Shared Components
Shared parameters are updated using momentum-based aggregation to stabilize training across heterogeneous clients:

\[
\theta_{\text{shared}}^{t+1} = \theta_{\text{shared}}^{t} + \eta \cdot \mathrm{Avg}\left(\Delta \theta_{\text{shared}}^{(k)}\right)
\]

where updates are averaged across participating clients in each round.

### 3. Class-Specific Momentum Buffering for Gaussian Priors
To mitigate drift in rarely observed classes under extreme non-IID settings, CMGA maintains a momentum buffer for each class prior:

- If class `c` is observed in the current round:
\[
\tilde{\mu}_c^{t+1} = \mathrm{Avg}\left(\mu_{k,c}\right), \quad
m_c^{t+1} = \beta m_c^t + (1 - \beta)\tilde{\mu}_c^{t+1}
\]

- Otherwise:
\[
m_c^{t+1} = m_c^t
\]

with momentum coefficient `β = 0.9`.

### 4. Proximal Inter-Class Separation Enforcement
To preserve a discriminative latent structure, CMGA enforces a minimum separation between class prior centers by solving:

\[
\mu_c^{t+1} = \arg\min_{\mu'} 
\frac{1}{2}\|\mu' - m_c^{t+1}\|^2
+ \lambda \sum_{j \neq c} \max(0, \delta - \|\mu' - \mu_j^{t+1}\|)
\]

- Minimum separation distance: `δ = 2.0`  
- Penalty weight: `λ = 0.1`  
- Optimization: 3 steps of Projected Gradient Descent (PGD)

### 5. Variance Collapse Prevention
To avoid posterior or variance collapse, a minimum variance constraint is enforced:
\[
\sigma_c^{t+1} = \max(\sigma_c^{t+1}, 0.1)
\]

## Why CMGA Outperforms Standard FedAvg
Under severe non-IID conditions, standard FedAvg degrades class-conditioned latent structures by indiscriminately averaging parameters.  
CMGA addresses this limitation by:
- Aggregating only components that benefit from global collaboration
- Stabilizing underrepresented classes via momentum buffering
- Explicitly enforcing inter-class separation in the latent space

These mechanisms enable **F-ACVAE** to achieve consistently superior performance compared to centralized baselines while fully preserving data privacy.

## Implementation in Flower (flwr)

CMGA is implemented as a custom strategy inheriting from `flwr.server.strategy.Strategy` (or extending `FedAvg` for shared components).  
The core logic resides in the `aggregate_fit` method:

```python
class CMGAStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        # 1. Aggregate shared components
        aggregated_shared = super().aggregate_fit(...)

        # 2. Extract class-conditioned Gaussian priors
        priors = extract_class_priors(results)

        # 3. Apply class-specific momentum buffering
        momentum_buffers = apply_class_momentum(priors, self.momentum_buffers)

        # 4. Enforce inter-class separation via proximal projection
        separated_means = proximal_projection(
            momentum_buffers, delta=2.0, lambda_=0.1
        )

        # 5. Clip variances to prevent collapse
        clipped_variances = clip_variances(separated_means)

        return new_global_parameters, {}
		
For the complete source code, refer to the implementation in the repository:
https://github.com/mohamad-ansarimehr/F-ACVAE (typically in strategy/cmga.py or equivalent).

## Reference
For full details, see Section "Constrained Momentum Gaussian Aggregation (CMGA)" in the paper:
**F-ACVAE: A Federated Adaptive Conditional Variational Auto-Encoder for Privacy-Preserving Intrusion Detection in IoT Networks**

Mohammad Ansarimehr, Somayeh Changiz, Ehsan Baghshani, Ali Mousavi (2025)
