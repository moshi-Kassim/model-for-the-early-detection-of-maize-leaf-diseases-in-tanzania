# EASTERN AFRICA STATISTICAL TRAINING CENTRE
## DATA SCIENCE AND INFORMATION TECHNOLOGY SECTION
### BACHELOR OF DATA SCIENCE (BDS) YEAR III

---

# DEVELOPING A PREDICTIVE DEEP LEARNING MODEL FOR THE EARLY DETECTION OF MAIZE LEAF DISEASES IN TANZANIA

**BY**

1. SEVERIA M. BANDA — EASTC/BDTS/24/01380  
2. MOSHI M. KASSIM — EASTC/BDTS/23/00309  
3. GIDION F. MACHUMU — EASTC/BDTS/23/00440  
4. REBECA P. SHAURI — EASTC/BDTS/24/01587  
5. EDGAR S. MATERU — EASTC/BDTS/24/01607  

**Academic Year:** 2025/2026  
**Supervisor:** Mr Kelvin Rushobola  
**Submission Date:** July 2026  

---

*This report was prepared in accordance with the **EASTC Data Science Project Writing Guidelines (Version 3, May 2025)**.*

---

## PRELIMINARY PAGES

### List of Abbreviations

| Abbreviation | Meaning |
|---|---|
| ANN | Artificial Neural Network |
| API | Application Programming Interface |
| CNN | Convolutional Neural Network |
| EASTC | Eastern Africa Statistical Training Centre |
| EDA | Exploratory Data Analysis |
| GUI | Graphical User Interface |
| RGB | Red, Green, Blue |
| RMSE | Root Mean Squared Error |
| SDG | Sustainable Development Goal |

### Table of Contents

1. [Chapter One: Introduction](#chapter-one-introduction)
2. [Chapter Two: Literature Review](#chapter-two-literature-review)
3. [Chapter Three: Methodology](#chapter-three-methodology)
4. [Chapter Four: Project Results and Discussion](#chapter-four-project-results-and-discussion)
5. [Chapter Five: Conclusion and Recommendations](#chapter-five-conclusion-and-recommendations)
6. [References](#references)
7. [Appendices](#appendices)

---

## CHAPTER ONE: INTRODUCTION

### 1.1 Background of the Study

Agriculture remains the backbone of the Tanzanian economy, employing approximately 55% of the national workforce (NBS & OCGS, 2024) and serving as the primary driver of national food security. The demand for food is growing exponentially while agricultural production remains insufficient in many areas. Farmers, scientists, researchers, analysts, specialists, and the government continue to implement strategies to increase agricultural production. One of the major causes of low yield is crop disease, which reduces the quality, quantity, and nutritional value of cereals and legumes; nearly 32% of losses in cereal crops are attributed to diseases (Savary et al., 2019).

At the centre of Tanzania's agricultural sector is maize (*Zea mays*), the most widely cultivated and consumed staple crop across both rural and urban populations. Maize is used for food, beverages, poultry feed, and cattle feed, but it is highly vulnerable to foliar diseases such as Common Rust, Northern Leaf Blight, and Cercospora Leaf Spot (Nsibo et al., 2024). These phytopathological threats can devastate entire harvests if not detected and managed during early stages.

Currently, disease detection relies heavily on manual field scouting and the visual expertise of agricultural extension officers. These traditional methods are slow, subjective, and constrained by the shortage of extension workers in Tanzania. By the time a farmer receives an expert diagnosis, the pathogen may have already spread beyond the point of effective intervention.

Recent advances in Artificial Intelligence and Data Science, particularly Computer Vision powered by Convolutional Neural Networks (CNNs), offer a new approach. Deep learning models can be trained on thousands of labelled plant images to recognize disease patterns from digital photographs (Mohanty et al., 2016; Khan et al., 2023). This project applies that capability to maize leaf disease detection and deploys the resulting model in a practical web-based diagnostic tool for Tanzanian agricultural stakeholders.

### 1.2 Statement of the Problem

Despite the critical importance of maize to Tanzania's food security, smallholder farmers face disproportionate yield losses due to the rapid and often undetected spread of foliar diseases such as Northern Leaf Blight and Common Rust. The fundamental problem lies in the structural bottleneck of traditional agricultural diagnostics, which relies almost entirely on human visual inspection.

Farmers who lack specialized phytopathological training must wait for extension officers to visit their often geographically isolated farms. Tanzania suffers from a severe deficit of extension workers, making timely expert evaluation rare during the crucial early stages of an outbreak. Without rapid and accurate disease identification, farmers frequently misapply broad-spectrum pesticides based on guesswork. This approach is financially burdensome, environmentally harmful, and allows pathogens to spread unchecked.

Laboratory-based diagnostics, while scientifically accurate, are centralized in urban research institutions and are inaccessible and too slow for rural farmers who require immediate intervention. There is therefore an urgent need for an automated, accessible, and low-cost diagnostic tool that can classify maize leaf diseases from digital images in real time.

This problem aligns with national development priorities under Tanzania's agricultural modernization agenda and global goals such as **SDG 2 (Zero Hunger)** and **SDG 9 (Industry, Innovation and Infrastructure)**, which promote food security and technological innovation.

### 1.3 General Objective

To develop a deep learning image classification model capable of automatically identifying and diagnosing common maize leaf diseases: Common Rust, Northern Leaf Blight, and Cercospora Leaf Spot, and to deploy the model in an interactive dashboard for real-time diagnosis.

### 1.4 Specific Objectives

1. To source a standardized dataset of healthy and diseased maize leaf images.
2. To train Convolutional Neural Network (CNN) models for classifying distinct maize foliar diseases.
3. To evaluate the algorithm's predictive performance using standard data science metrics (Accuracy, Precision, Recall, F1-Score, and Confusion Matrix).
4. To deploy the trained prediction model into an interactive graphical user interface (dashboard) for real-time image diagnosis.

### 1.5 Research Questions

1. What image preprocessing techniques are required to optimize raw leaf data for deep learning ingestion?
2. How accurately can a Convolutional Neural Network classify different maize leaf disease classes?
3. How can the predictive model be effectively deployed to accept new, unseen images and output real-time diagnostic confidence scores?

### 1.6 Significance of the Study

This study contributes to the collective effort to protect food security and enhance agricultural productivity in Tanzania by modernizing how maize diseases are detected and managed. By overcoming the limitations of traditional diagnostic methods, the project enables early and precise detection of foliar disease symptoms from leaf photographs.

The study has academic significance by demonstrating the application of computer vision and deep learning in agricultural data science. It has practical significance by providing farmers and extension officers with a deployable diagnostic tool. Technologically, the project bridges the gap between model development and practical deployment, addressing a common limitation in existing plant disease research.

### 1.7 Scope of the Project

This project is scoped as follows:

- **Domain:** Agricultural computer vision / predictive analytics  
- **Geographical focus:** Tanzania (with dataset from global PlantVillage repository)  
- **Crop:** Maize (*Zea mays*) leaves only  
- **Disease classes:** Healthy, Common Rust, Northern Leaf Blight, Cercospora Leaf Spot  
- **Data type:** Secondary digital RGB images  
- **Sample size:** 4,188 labelled images  
- **Deployment:** Streamlit web dashboard running locally  
- **Timeframe:** Academic Year 2025/2026  

The project does not cover root diseases, soil analysis, or multi-crop classification.

---

## CHAPTER TWO: LITERATURE REVIEW

### 2.1 Definition of Key Terms

**Maize Leaf Disease:** A pathological condition affecting maize foliage caused by fungi, bacteria, or viruses, manifesting as visible lesions, discoloration, or rust pustules on leaf tissue (Nsibo et al., 2024).

**Convolutional Neural Network (CNN):** A deep learning architecture designed to process grid-like data such as images by applying convolutional filters that automatically learn spatial features including edges, textures, and disease patterns (Wu, 2017).

**Transfer Learning:** A machine learning approach where a model pre-trained on a large dataset (e.g., ImageNet) is adapted to a new task by reusing its learned features and training only selected layers (Too et al., 2019).

**PlantVillage Dataset:** An open-source, peer-reviewed repository of labelled plant leaf images widely used for training and benchmarking plant disease classification models (Mohanty et al., 2016).

**Precision and Recall:** Classification metrics where precision measures the proportion of correct positive predictions among all positive predictions, and recall measures the proportion of actual positive cases correctly identified.

### 2.2 Theoretical Framework

The computational diagnosis of agricultural diseases relies on a shift from rule-based programming to data-driven learning. This study is underpinned by two foundational theories in Artificial Intelligence:

**Connectionism (Artificial Neural Networks):** Connectionism models mental or behavioural phenomena as emergent processes of interconnected networks of simple units (Medler, 1998). In this project, artificial neurons receive pixel inputs, apply mathematical weights, and pass signals through layers until a disease classification is produced.

**Representation Learning (via CNNs):** Representation learning posits that a system can automatically discover the features needed for classification from raw data (Noroozi et al., 2017). CNNs apply this theory to images by learning hierarchical features from simple edges to complex disease patterns. This justifies the use of raw RGB leaf images rather than manually engineered features.

**Relevance and Limitations:** These theories are highly effective for visual classification but are data-dependent and operate as "black-box" models that provide statistical probabilities rather than explicit biological explanations.

### 2.3 Empirical Framework

**Baseline Deep Learning Feasibility (Mohanty et al., 2016):** Trained AlexNet and GoogLeNet on 54,306 PlantVillage images and achieved 99.35% accuracy, establishing that deep learning can classify plant diseases under controlled conditions. This validates the use of PlantVillage data in the current project.

**Architectural Optimization (Too et al., 2019):** Compared VGG16, Inception V4, ResNet, and DenseNet using transfer learning. DenseNet achieved 99.75% accuracy with fewer parameters, informing the decision to evaluate transfer learning architectures such as ResNet50.

**Mobile Deployment in African Agriculture (Ramcharan et al., 2019):** Deployed MobileNet on smartphones for cassava disease detection in East Africa with 89% field accuracy, demonstrating that AI diagnostics are viable in African agricultural contexts despite performance drops from laboratory to field conditions.

**Patterns and Contradictions:** Laboratory accuracies often exceed 95%, but field deployment frequently shows lower performance due to varied lighting, backgrounds, and image quality. A persistent gap exists between model development and accessible deployment tools.

### 2.4 Research Gap

Existing studies frequently stop at algorithmic evaluation without delivering accessible tools for end users. Many models remain in code repositories or research papers without practical interfaces for farmers or extension officers. Furthermore, most studies do not address rejection of non-target images (e.g., other crops uploaded by mistake).

This project addresses the gap by:
1. Building and comparing CNN architectures on maize-specific data  
2. Deploying the best model in a Streamlit dashboard  
3. Adding image validation rules to reject non-maize uploads  

### 2.5 Conceptual Framework

The conceptual framework defines the relationship among key variables:

**Independent Variable:** Maize leaf image features (RGB pixel data, lesion geometry, colour gradients, textures).

**Intervening Variable:** CNN architecture and training process (convolution layers, pooling, dense layers, softmax output).

**Dependent Variable:** Disease classification output comprising:
- Categorical label (Healthy, Common Rust, Northern Leaf Blight, Cercospora Leaf Spot)  
- Confidence score (percentage probability)

**Process Flow:**

```
Maize Leaf Image → Preprocessing → CNN Model → Disease Label + Confidence Score → Streamlit Dashboard Display
```

---

## CHAPTER THREE: METHODOLOGY

### 3.1 Study Area

- **Geographical context:** Tanzania (application area)  
- **Domain:** Agriculture / Plant pathology / Computer vision  
- **Institution:** Eastern Africa Statistical Training Centre (EASTC)  
- **Problem owners:** Smallholder maize farmers and agricultural extension officers  
- **Deployment environment:** Local web browser via Streamlit application  

### 3.2 Project Approach

This project follows a **Predictive Analytics** and **Computer Vision** approach (EASTC Guidelines, Table 1, Categories 3 and 8). The workflow includes data acquisition, preprocessing, model training, evaluation, and deployment of a diagnostic web application.

**Tools and Technologies:**
- Python 3.10+  
- TensorFlow / Keras  
- OpenCV, NumPy, Pandas  
- Streamlit  
- scikit-learn (evaluation metrics)  

### 3.3 Population and Sample

**Population:** All labelled maize leaf images in the PlantVillage maize subset on Kaggle.

**Sample:** 4,188 RGB images categorized into four classes:
1. Healthy  
2. Common Rust (*Puccinia sorghi*)  
3. Northern Leaf Blight (*Exserohilum turcicum*)  
4. Cercospora Leaf Spot (*Cercospora zeae-maydis*)  

**Sampling technique:** Stratified random split to preserve class proportions across training, validation, and test sets.

| Dataset Split | Images | Percentage |
|---|---|---|
| Training | 2,931 | 70% |
| Validation | 628 | 15% |
| Test | 629 | 15% |
| **Total** | **4,188** | **100%** |

*Note: The original proposal planned an 80/10/10 split. During implementation, a 70/15/15 stratified split was adopted to provide adequate validation and test samples for reliable evaluation.*

### 3.4 Sources and Instruments for Data Collection

**Data source:** Secondary data from the open-source PlantVillage dataset (Kaggle).

**Instruments:**
- Jupyter Notebook (`corn-cnn.ipynb`) for model development  
- Python scripts and Streamlit application (`app.py`) for deployment  
- Saved model file: `corn_disease_cnn.h5`  

No primary field data collection or human subjects were involved.

### 3.5 Data Preprocessing

Preprocessing steps applied during training and deployment:

1. **Resizing:** All images resized to 128 × 128 pixels  
2. **Colour conversion:** RGB to BGR format to match training pipeline  
3. **Normalization:** Pixel values scaled from 0–255 to 0–1  
4. **Batch formatting:** Images shaped as (1, 128, 128, 3) for model input  

Data augmentation was explored during training notebook development to reduce overfitting.

### 3.6 Models and Algorithms

Two models were developed and compared:

#### 3.6.1 Custom CNN (Selected Model)

A convolutional neural network built from scratch:

```
Input (128×128×3)
→ Conv2D(32) → Conv2D(32) → MaxPool → Dropout
→ Conv2D(64) → Conv2D(64) → MaxPool → Dropout
→ Conv2D(128) → MaxPool → Dropout
→ Flatten → Dense(256) → Dropout
→ Dense(4, softmax)
```

- **Optimizer:** Adam  
- **Loss:** Sparse Categorical Cross-Entropy  
- **Epochs:** 25  
- **Batch size:** 32  

#### 3.6.2 ResNet50 (Baseline Comparison)

Transfer learning model using ResNet50 pre-trained on ImageNet:
- Base layers frozen  
- Custom classification head: GlobalAveragePooling → Dense(256) → Dense(128) → Dense(4)  
- **Optimizer:** Adam (learning rate 0.0001)  
- **Epochs:** 100  

**Justification for model selection:** Both models were evaluated on the same test set. The Custom CNN achieved higher accuracy (92.37% vs 77.42%) and was selected for deployment.

### 3.7 Model Training and Validation

- Training performed on 2,931 images  
- Validation used during training to monitor loss and accuracy  
- Final evaluation on held-out test set of 629 images never seen during training  
- **Evaluation metrics:** Accuracy, Loss, Precision, Recall, F1-Score, Confusion Matrix  

### 3.8 Deliverables

1. Trained Custom CNN model (`corn_disease_cnn.h5`)  
2. Streamlit web dashboard for real-time diagnosis  
3. Image validation module for non-maize rejection  
4. Model performance report and confusion matrix  
5. Project documentation and source code (GitHub repository)  

### 3.9 Ethical Considerations

This study uses open-source, de-identified secondary data (plant images only). No human subjects, personal data, or animal testing were involved. All datasets, pre-trained architectures, and software libraries are properly referenced. Academic integrity and plagiarism guidelines of EASTC were followed.

### 3.10 Project Timeline

| Phase | Activity | Duration |
|---|---|---|
| 1 | Proposal writing and approval | Month 1 |
| 2 | Literature review and dataset sourcing | Month 1–2 |
| 3 | Data preprocessing and EDA | Month 2 |
| 4 | Model training (Custom CNN and ResNet50) | Month 2–3 |
| 5 | Model evaluation and comparison | Month 3 |
| 6 | Dashboard development (Streamlit) | Month 3–4 |
| 7 | Testing, validation rules, and refinement | Month 4 |
| 8 | Report writing and submission | Month 4–5 |

---

## CHAPTER FOUR: PROJECT RESULTS AND DISCUSSION

### 4.1 Pre-processing Results

All 4,188 images were successfully loaded, resized to 128 × 128 pixels, and normalized. Exploratory analysis confirmed four balanced disease classes in the maize subset. Stratified splitting ensured each class was represented proportionally in training, validation, and test sets.

### 4.2 Results by Specific Objective

#### Specific Objective 1: To source a standardized dataset of healthy and diseased maize leaf images

**Result:** A total of 4,188 labelled maize leaf images were obtained from the PlantVillage dataset, covering four classes: Healthy, Common Rust, Northern Leaf Blight, and Cercospora Leaf Spot.

**Interpretation:** The dataset provided sufficient labelled samples for CNN training and met the requirement for standardized, peer-reviewed agricultural imagery.

#### Specific Objective 2: To train CNN models for classifying distinct maize foliar diseases

**Result:** Two models were trained — a Custom CNN (25 epochs) and a ResNet50 transfer learning model (100 epochs, frozen base). The Custom CNN was selected for deployment after outperforming ResNet50 on the test set.

**Interpretation:** For this dataset size and task, a task-specific Custom CNN learned maize disease patterns more effectively than a frozen pre-trained ResNet50 architecture.

#### Specific Objective 3: To evaluate predictive performance using standard metrics

**Result:**

| Model | Test Accuracy | Test Loss |
|---|---|---|
| **Custom CNN** | **92.37%** | **0.3725** |
| ResNet50 | 77.42% | 0.5277 |

**Per-class metrics (Custom CNN):**

| Class | Precision | Recall | F1-Score |
|---|---|---|---|
| Common Rust | 0.97 | 0.96 | 0.97 |
| Northern Leaf Blight | 0.83 | 0.94 | 0.88 |
| Healthy | 1.00 | 1.00 | 1.00 |
| Cercospora Leaf Spot | 0.85 | 0.65 | 0.74 |

**Confusion Matrix (Custom CNN — test set):**

| Actual \ Predicted | NLB | Rust | CLS | Healthy |
|---|---|---|---|---|
| Northern Leaf Blight | 162 | 5 | 5 | 0 |
| Common Rust | 3 | 188 | 5 | 0 |
| Cercospora Leaf Spot | 22 | 8 | 56 | 0 |
| Healthy | 0 | 0 | 0 | 175 |

**Interpretation:** The model performs excellently on Healthy and Common Rust classes. Northern Leaf Blight shows good recall (0.94) but moderate precision (0.83). Cercospora Leaf Spot is the most challenging class, with recall of 0.65, often confused with Northern Leaf Blight (22 misclassifications). Overall test accuracy of 92.37% demonstrates strong predictive capability on unseen data.

#### Specific Objective 4: To deploy the model in an interactive dashboard

**Result:** A Streamlit web application was developed with three main sections:
- **Diagnose:** Upload maize leaf image → automatic prediction with confidence score, probability bars, symptoms, and management advice  
- **Performance:** Display model metrics, confusion matrix, and model comparison  
- **About:** Project information and usage instructions  

Additional validation rules were implemented to reject non-maize images (e.g., mango, banana, sugarcane) before displaying results.

**Interpretation:** The deployment objective was achieved. The dashboard transforms the trained model from a research artifact into a functional diagnostic tool accessible through a web browser.

### 4.3 Discussion

The results confirm that deep learning can effectively classify maize leaf diseases from digital images, consistent with findings by Mohanty et al. (2016) and Too et al. (2019). However, the lower performance of ResNet50 compared to the Custom CNN suggests that for a focused four-class problem with ~4,000 images, a simpler task-specific architecture may outperform a frozen general-purpose deep network.

The confusion between Cercospora Leaf Spot and Northern Leaf Blight reflects visual similarity in lesion appearance and is consistent with challenges reported in phytopathological literature (Nsibo et al., 2024). Healthy and Common Rust classifications were near-perfect on the test set.

The validation module addresses a practical limitation not covered in many laboratory studies: users may upload non-maize images. Rule-based checks on colour, texture, and symptom consistency improved real-world usability.

Comparison with Ramcharan et al. (2019), who achieved 89% field accuracy for cassava on mobile devices, suggests this project's 92.37% laboratory accuracy is competitive, though field validation on Tanzanian farm images remains necessary.

**Limitations:**
- Dataset images are from controlled PlantVillage conditions, not Tanzanian field environments  
- Model input size (128×128) may lose fine lesion detail  
- Cercospora Leaf Spot recall needs improvement  
- Dashboard requires a computer; mobile deployment was not completed in this phase  

---

## CHAPTER FIVE: CONCLUSION AND RECOMMENDATIONS

### 5.1 Conclusion

This project successfully developed and deployed a deep learning system for early detection of maize leaf diseases in Tanzania. The specific objectives were met as follows:

1. A standardized dataset of 4,188 maize leaf images was sourced from PlantVillage.  
2. Custom CNN and ResNet50 models were trained; the Custom CNN achieved 92.37% test accuracy.  
3. Model performance was evaluated using accuracy, precision, recall, F1-score, and confusion matrix.  
4. The model was deployed in a Streamlit dashboard for real-time image diagnosis.  

The project demonstrates that a task-specific Custom CNN, combined with a user-friendly web interface, can provide an accessible diagnostic support tool for maize foliar diseases. The system supports SDG 2 (Zero Hunger) by contributing to improved crop disease management and food security in Tanzania.

### 5.2 Recommendations

1. **Extension services:** Tanzania's Ministry of Agriculture and local extension officers should pilot the dashboard as a supplementary diagnostic tool alongside expert field inspection.  
2. **Field validation:** Collect maize leaf images from Tanzanian farms to retrain and validate the model under real field conditions.  
3. **Mobile deployment:** Convert the model to a lightweight mobile application (e.g., TensorFlow Lite) for offline use by rural farmers.  
4. **Model improvement:** Increase Cercospora Leaf Spot training samples and apply data augmentation to improve recall for that class.  
5. **Farmer training:** Provide brief user guides on capturing clear, single-leaf photographs for best diagnostic accuracy.  

### 5.3 Future Work

- Collect and label Tanzanian field images for domain adaptation  
- Fine-tune ResNet50 with unfrozen layers for comparison under larger datasets  
- Integrate multilingual support (Kiswahili) in the dashboard  
- Add GPS-based farm location logging for disease outbreak mapping  
- Explore model compression for deployment on low-cost Android devices  

---

## REFERENCES

Khan, F., Zafar, N., Tahir, M. N., Aqib, M., Waheed, H., & Haroon, Z. (2023). A mobile-based system for maize plant leaf disease detection and classification using deep learning. *Frontiers in Plant Science*, *14*(May), 1–18. https://doi.org/10.3389/fpls.2023.1079366

Mahlein, A.-K. (2016). Present and Future Trends in Plant Disease Detection. *Plant Disease*, *100*(2), 1–11. https://doi.org/10.1007/s13398-014-0173-7.2

Medler, D. A. (1998). A Brief History of Connectionism. *Neural Computing Surveys*, *1*(2), 18–72. https://doi.org/10.1007/BF01889762

Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016). Using deep learning for image-based plant disease detection. *Frontiers in Plant Science*, *7*(September), 1–10. https://doi.org/10.3389/fpls.2016.01419

NBS [National Bureau of Statistics], & OCGS [Office of the Chief Government Statistician]. (2024). *Tanzania Integrated Labour Force Survey 2024 Report*.

Noroozi, M., Pirsiavash, H., & Favaro, P. (2017). Representation Learning by Learning to Count. *Proceedings of the IEEE International Conference on Computer Vision*, 5899–5907. https://doi.org/10.1109/ICCV.2017.628

Nsibo, D. L., Barnes, I., & Berger, D. K. (2024). Recent advances in the population biology and management of maize foliar fungal pathogens *Exserohilum turcicum*, *Cercospora zeina* and *Bipolaris maydis* in Africa. *Frontiers in Plant Science*, *15*(August), 1–23. https://doi.org/10.3389/fpls.2024.1404483

Ramcharan, A., McCloskey, P., Baranowski, K., Mbilinyi, N., Mrisho, L., Ndalahwa, M., Legg, J., & Hughes, D. P. (2019). A mobile-based deep learning model for cassava disease diagnosis. *Frontiers in Plant Science*, *10*(March), 1–8. https://doi.org/10.3389/fpls.2019.00272

Savary, S., Willocquet, L., Pethybridge, S. J., Esker, P., McRoberts, N., & Nelson, A. (2019). The global burden of pathogens and pests on major food crops. *Nature Ecology & Evolution*, *3*(3), 430–439. https://doi.org/10.1038/s41559-018-0793-y

Too, E. C., Yujian, L., Njuki, S., & Yingchun, L. (2019). A comparative study of fine-tuning deep learning models for plant disease identification. *Computers and Electronics in Agriculture*, *161*, 272–279. https://doi.org/10.1016/j.compag.2018.03.032

Wu, J. (2017). *Introduction to Convolutional Neural Networks*. Nanjing University.

---

## APPENDICES

### Appendix A: Custom CNN Architecture Summary

| Layer | Output Shape | Parameters |
|---|---|---|
| Conv2D (32 filters) | 128 × 128 × 32 | 896 |
| Conv2D (32 filters) | 128 × 128 × 32 | 9,248 |
| MaxPooling2D | 64 × 64 × 32 | 0 |
| Conv2D (64 filters) | 64 × 64 × 64 | 18,496 |
| Conv2D (64 filters) | 64 × 64 × 64 | 36,928 |
| MaxPooling2D | 32 × 32 × 64 | 0 |
| Conv2D (128 filters) | 32 × 32 × 128 | 73,856 |
| MaxPooling2D | 16 × 16 × 128 | 0 |
| Flatten + Dense(256) | 256 | 8,388,864 |
| Dense(4, softmax) | 4 | 1,028 |

### Appendix B: Streamlit Dashboard Pages

1. **Diagnose** — Image upload, automatic prediction, rejection of non-maize images  
2. **Performance** — Accuracy metrics, per-class scores, confusion matrix  
3. **About** — Project objectives, methodology, and disease class descriptions  

### Appendix C: How to Run the Application

```bash
cd "python dashboard"
pip install -r requirements.txt
streamlit run app.py
```

Open browser at: `http://localhost:8501`

### Appendix D: GitHub Repository

Project source code: https://github.com/moshi-Kassim/Maize-Leaf-Disease-Detection

---

*Prepared in accordance with EASTC Data Science Project Writing Guidelines Version 3 (May 2025).*
