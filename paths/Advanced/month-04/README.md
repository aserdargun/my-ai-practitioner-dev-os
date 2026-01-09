# Month 04 — Computer Vision

Master CNN architectures and object detection.

---

## Why It Matters

Computer vision enables machines to understand visual content. From autonomous vehicles to medical imaging, CV skills are in high demand. Understanding CNNs and modern detection systems like YOLO is essential for building visual AI applications.

---

## Prerequisites

- PyTorch proficiency (Month 02-03)
- Understanding of neural network training
- Basic image processing concepts
- Linear algebra fundamentals

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 1 Focus
- **YOLO**: Real-time object detection

### Tier 2 Focus
- **CNN**: Convolutional neural network architectures
- **GAN**: Generative adversarial networks
- **OpenCV**: Image processing and manipulation

### Concepts
- Convolution operations
- Pooling and feature extraction
- Object detection vs classification
- Bounding boxes and IoU
- Transfer learning for vision
- Image augmentation

---

## Main Project: Object Detection System

Build a complete object detection pipeline.

### Deliverables

1. **Image Classifier**
   - CNN from scratch
   - Transfer learning with pretrained backbone
   - Multi-class classification

2. **Object Detector**
   - YOLO implementation or usage
   - Real-time detection demo
   - Custom object training

3. **Image Processing Pipeline**
   - OpenCV preprocessing
   - Augmentation pipeline
   - Batch processing

4. **Documentation**
   - Architecture diagrams
   - Training methodology
   - Results visualization

### Definition of Done

- [ ] CNN classifier achieves > 85% accuracy
- [ ] YOLO detects objects in real-time
- [ ] Custom training on at least one new class
- [ ] OpenCV pipeline processes images correctly
- [ ] Demo video showing detection
- [ ] Documentation covers architecture and training

---

## Stretch Goals

- [ ] Implement GAN for image generation
- [ ] Build semantic segmentation model
- [ ] Deploy detection model with FastAPI
- [ ] Real-time webcam detection
- [ ] Compare YOLOv5, v7, v8 performance

---

## Weekly Breakdown

### Week 1: CNN Foundations
- Convolution operations
- Building CNN from scratch
- Image classification task
- Data augmentation

### Week 2: Transfer Learning
- Using pretrained models
- Fine-tuning strategies
- Feature extraction
- Model comparison

### Week 3: Object Detection
- YOLO architecture
- Setting up detection pipeline
- Training on custom data
- Evaluation metrics (mAP)

### Week 4: Integration & Polish
- OpenCV preprocessing
- Real-time demo
- Documentation
- Portfolio-ready project

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 4 focusing on computer vision. Help me plan a week learning CNNs and building a classifier.
```

### Building
```
As the Builder agent, help me set up YOLO for custom object detection. I want to detect [specific objects].
```

### Understanding
```
As the Researcher, explain how convolution operations extract features from images. Include visualizations.
```

### Debugging
```
/debug-learning — My CNN is overfitting. Loss is low on training but high on validation. How do I fix this?
```

### Detection Help
```
As the Builder, help me implement real-time webcam object detection using YOLO and OpenCV.
```

---

## How to Publish

### Demo
- Show image classification on various inputs
- Real-time object detection video
- Custom trained detector results
- Processing speed metrics

### Write-up Topics
- How CNNs see images
- From classification to detection
- Transfer learning magic
- YOLO architecture overview

---

## Resources

### Documentation
- [PyTorch Vision](https://pytorch.org/vision/stable/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Ultralytics YOLO](https://docs.ultralytics.com/)

### Papers
- "ImageNet Classification with Deep CNNs" (AlexNet)
- "You Only Look Once: Unified, Real-Time Object Detection"
- "Deep Residual Learning" (ResNet)

### Datasets
- CIFAR-10/100
- ImageNet (subset)
- COCO (for detection)
- Custom dataset creation

---

## Next Month Preview

**Month 05**: RAG Systems — Building retrieval-augmented generation with LangChain, vector databases, and embeddings.
