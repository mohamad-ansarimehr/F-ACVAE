# Constrained Momentum Gaussian Aggregation (CMGA)

**Constrained Momentum Gaussian Aggregation (CMGA)** is a custom server-side aggregation strategy developed specifically for the federated extension of the **Constrained Twin Variational Auto-Encoder (CTVAE)** in the F-CTVAE framework. It is implemented as a custom Flower (`flwr`) Strategy and replaces conventional FedAvg to address the destructive effects of naive parameter averaging on the discriminative latent structure under severe non-IID conditions.

CMGA enables selective aggregation, preserves class-conditioned Gaussian priors, and actively enforces inter-class separation, resulting in both **superior detection performance** and a **62% reduction in communication overhead**.

## Core Mechanisms

### 1. Selective Parameter Aggregation
Only the shared, globally beneficial components are uploaded and aggregated:
- Hermaphrodite Mapper (`H`)
- Decoder (`D`)
- Class-specific Gaussian prior parameters: `{μ_c, log σ²_c}` for each class `c = 1, ..., C`

**Local encoders (`E`)** remain **strictly private** on each client and are never transmitted.

**Benefit**: Reduces communicated parameters from ~8.7M to ~3.3M per client per round (~62% bandwidth savings).

### 2. Momentum-Enhanced Update for Shared Components
The hermaphrodite mapper and decoder are updated using standard momentum-based averaging:
θ_shared^{t+1} = θ_shared^t + η × average(Δθ_shared across participating clients)

### 3. Class-Specific Momentum Buffering for Gaussian Priors
Prevents drift of rarely observed attack classes in highly skewed non-IID settings:
If class c is observed in the current round:
μ̃_c^{t+1} = weighted average of μ_{k,c} from clients that observed class c
m_c^{t+1} = β × m_c^t + (1 - β) × μ̃_c^{t+1}    (β = 0.9)
Else:
m_c^{t+1} = m_c^t   (preserve previous momentum value)

### 4. Proximal Inter-Class Separation Enforcement
Explicitly maintains a minimum separation between class prior centers in latent space:
μ_c^{t+1} = argmin_{μ'} (1/2)‖μ' - m_c^{t+1}‖²

λ × Σ_{j≠c} max(0, δ - ‖μ' - μ_j^{t+1}‖)

- Minimum separation distance: `δ = 2.0`
- Penalty weight: `λ = 0.1`
- Optimization solved with 3 steps of Projected Gradient Descent (PGD)

- Minimum separation distance: `δ = 2.0`
- Penalty weight: `λ = 0.1`
- Optimization solved with 3 steps of Projected Gradient Descent (PGD)

### 5. Variance Collapse Prevention
Avoids posterior collapse by enforcing a minimum variance:
σ_c^{t+1} = max(σ_c^{t+1}, 0.1)

## Why CMGA Outperforms Standard FedAvg
Standard FedAvg destroys the carefully learned discriminative structure of CTVAE under extreme non-IID conditions. CMGA counters this by:
- Aggregating only components that benefit from global collaboration
- Stabilizing rarely seen classes via momentum buffering
- Actively enforcing structured separation in latent space

These mechanisms collectively enable F-CTVAE to **surpass centralized CTVAE** in macro F1-score while preserving full raw-data privacy.

## Implementation in Flower (flwr)

CMGA is implemented as a custom strategy inheriting from `flwr.server.strategy.Strategy` (often extending `FedAvg` for shared components). The core logic is in the `aggregate_fit` method:

```python
class CMGAStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        # 1. Aggregate shared components (H and D)
        aggregated_shared = super().aggregate_fit(...)  # or custom weighted averaging

        # 2. Extract class-specific Gaussian priors from client updates
        priors = extract_class_priors(results)

        # 3. Apply class-specific momentum buffering
        momentum_buffers = apply_class_momentum(priors, self.momentum_buffers)

        # 4. Enforce inter-class separation via proximal projection
        separated_means = proximal_projection(momentum_buffers, delta=2.0, lambda_=0.1)

        # 5. Clip variances to prevent collapse
        clipped_variances = clip_variances(separated_means)

        # Combine updated shared parameters and priors into new global model
        return new_global_parameters, {}
```
		
For the complete source code, refer to the implementation in the repository:
https://github.com/mohamad-ansarimehr/F-CTVAE (typically in strategy/cmga.py or equivalent).

## Reference
For full details, see Section "Constrained Momentum Gaussian Aggregation (CMGA)" in the paper:
**F-CTVAE: A Federated Constrained Twin VAE for Privacy-Preserving Intrusion Detection in IoT Networks**
Ali Mousavi, Somayeh Changiz, Ehsan Baghshani, Mohammad Ansarimehr (2025)