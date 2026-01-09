# Month 11 — Performance

Optimize ML models for speed and efficiency.

---

## Why It Matters

Production ML systems need to be fast and efficient. Understanding GPU programming, model optimization, and inference acceleration separates senior ML engineers from beginners. This month covers the techniques that enable real-time AI at scale.

---

## Prerequisites

- Strong Python programming
- Deep learning experience (PyTorch/TensorFlow)
- Month 08: MLOps (deployment basics)
- Basic understanding of computer architecture

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 3 Focus
- **CUDA**: GPU programming
- **ONNX**: Model interchange format
- **TensorRT**: NVIDIA inference optimizer
- **TFLite**: Mobile/edge deployment

### Concepts
- GPU architecture and memory hierarchy
- Model quantization (INT8, FP16)
- Graph optimization
- Kernel fusion
- Batching strategies
- Memory optimization
- Latency vs throughput trade-offs

---

## Main Project: Optimized Inference System

Build a high-performance ML inference system.

### Deliverables

1. **ONNX Conversion**
   - PyTorch to ONNX export
   - TensorFlow to ONNX export
   - Model validation
   - Performance baseline

2. **TensorRT Optimization**
   - TensorRT engine building
   - FP16/INT8 quantization
   - Dynamic batching
   - Performance profiling

3. **CUDA Custom Operations**
   - Custom CUDA kernel
   - Memory optimization
   - Profiling with Nsight
   - Integration with PyTorch

4. **Edge Deployment**
   - TFLite conversion
   - Model pruning
   - On-device inference
   - Battery/memory constraints

### Definition of Done

- [ ] ONNX model exports correctly
- [ ] TensorRT achieves 3x+ speedup
- [ ] Custom CUDA kernel works
- [ ] TFLite runs on mobile/edge device
- [ ] Latency benchmarks documented
- [ ] Optimization trade-offs analyzed

---

## Stretch Goals

- [ ] Implement dynamic batching server
- [ ] Add model distillation
- [ ] Build CUDA extension for PyTorch
- [ ] Deploy to Jetson device
- [ ] Compare inference frameworks (TensorRT vs OpenVINO vs ONNX Runtime)

---

## Weekly Breakdown

### Week 1: ONNX & Model Export
- ONNX format deep dive
- Exporting from PyTorch
- Exporting from TensorFlow
- Model validation

### Week 2: TensorRT Optimization
- TensorRT basics
- Building engines
- Quantization
- Performance profiling

### Week 3: CUDA Programming
- CUDA architecture
- Basic kernels
- Memory optimization
- PyTorch integration

### Week 4: Edge & Production
- TFLite deployment
- Production optimization
- Benchmarking
- Documentation

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 11 focusing on performance. Help me plan a week learning ONNX and TensorRT optimization.
```

### Building
```
As the Builder agent, help me convert my PyTorch model to ONNX and optimize it with TensorRT.
```

### CUDA
```
As the Builder, help me write a custom CUDA kernel for [specific operation]. I need to understand the memory access patterns.
```

### Understanding
```
As the Researcher, explain how TensorRT optimizes neural networks. Include graph fusion and quantization.
```

### Debugging
```
/debug-learning — My ONNX export fails with dynamic shapes. How do I handle variable-length inputs?
```

---

## How to Publish

### Demo
- Before/after latency comparison
- GPU utilization visualization
- Edge device deployment
- Real-time inference demo

### Write-up Topics
- Why model optimization matters
- ONNX ecosystem explained
- TensorRT optimization guide
- CUDA basics for ML engineers

---

## Resources

### Documentation
- [ONNX Docs](https://onnx.ai/onnx/)
- [TensorRT Docs](https://developer.nvidia.com/tensorrt)
- [CUDA Toolkit Docs](https://docs.nvidia.com/cuda/)
- [TFLite Docs](https://www.tensorflow.org/lite)

### Tutorials
- NVIDIA Deep Learning Institute courses
- "Optimizing ML Models for Production"
- "CUDA by Example"

### Tools
- Netron (model visualization)
- NVIDIA Nsight
- PyTorch Profiler
- ONNX Runtime

---

## Next Month Preview

**Month 12**: Advanced ML — Graph neural networks, reinforcement learning, and federated learning.
