# 연구 분석 문서화 체계 (Bioinformatics & Scientific Research)

## 📬 연구 보고서 구조

### 디렉토리 체계
```
docs/
└── analysis/
    ├── research/           # 🧬 연구 분석 보고서
    │   ├── transcriptome/  # 전사체 분석
    │   ├── genomics/       # 유전체 분석
    │   ├── proteomics/     # 단백체 분석
    │   ├── metabolomics/   # 대사체 분석
    │   ├── clinical/       # 임상 데이터 분석
    │   └── integrated/     # 통합 오믹스 분석
    └── figures/            # 📊 그림과 플롯
        ├── heatmaps/       # 히트맵
        ├── volcano/        # 볼케이노 플롯
        ├── pca/            # PCA 플롯
        └── networks/       # 네트워크 다이어그램
```

## 🧬 연구 분석 프롬프트

### 1. 전사체 분석 (/분석 transcriptome)
```markdown
"RNA-seq 데이터의 DEG 분석 결과를 정리하고
pathway enrichment와 함께 보고서 작성해줘.
대조군 vs 처리군 비교, FDR < 0.05 기준"
```

### 2. 유전체 변이 분석 (/분석 genomics)
```markdown
"WGS/WES 데이터의 변이 분석 결과를 정리하고
pathogenic variants를 ACMG 가이드라인에 따라 분류해줘"
```

### 3. 단백체 분석 (/분석 proteomics)
```markdown
"Mass spec 데이터의 differential expression 분석하고
GO enrichment와 protein-protein interaction 네트워크 구성해줘"
```

### 4. 통합 오믹스 (/분석 integrated)
```markdown
"Multi-omics 데이터를 통합 분석하고
molecular signature와 biomarker candidates 도출해줘"
```

## 📄 연구 보고서 템플릿

### 전사체 분석 보고서 표준
```markdown
# [프로젝트명] 전사체 분석 보고서

## 1. 연구 개요 (Study Overview)
- **목적**: [연구 목적 및 가설]
- **샘플**: [샘플 수, 그룹 구성]
- **플랫폼**: [Illumina NovaSeq, etc.]
- **분석일**: YYYY-MM-DD

## 2. 방법론 (Methods)
### 2.1 시퀀싱 및 품질 관리
- Read quality filtering (FastQC)
- Trimming parameters (Trimmomatic/fastp)
- Alignment statistics (STAR/HISAT2)

### 2.2 발현량 정량화
- Reference genome: [GRCh38/mm10]
- Quantification: [RSEM/featureCounts]
- Normalization: [TPM/FPKM/DESeq2]

### 2.3 차등발현유전자 분석
- Statistical method: [DESeq2/edgeR]
- Cutoff: |log2FC| > 1, FDR < 0.05
- Multiple testing correction: [BH/Bonferroni]

## 3. 결과 (Results)
### 3.1 품질 관리 메트릭
| Sample | Raw Reads | Clean Reads | Mapping Rate | RIN |
|--------|-----------|-------------|--------------|-----|
| S1     | 50M       | 48M         | 95.2%        | 8.5 |

### 3.2 차등발현유전자 (DEGs)
- **상향조절**: N개 유전자
- **하향조절**: N개 유전자
- **Top 20 DEGs 테이블**

### 3.3 기능 분석 (Functional Analysis)
#### GO Enrichment
| GO Term | Category | p-value | Genes |
|---------|----------|---------|-------|

#### KEGG Pathway
| Pathway | p-value | Genes | Visualization |
|---------|---------|-------|---------------|

### 3.4 주요 발견사항
1. [핵심 발견 1]
2. [핵심 발견 2]
3. [핵심 발견 3]

## 4. 시각화 (Visualizations)
- **Figure 1**: Volcano plot of DEGs
- **Figure 2**: Heatmap of top 50 DEGs
- **Figure 3**: PCA plot
- **Figure 4**: Pathway enrichment dot plot

## 5. 해석 및 논의 (Interpretation)
### 5.1 생물학적 의미
### 5.2 기존 연구와 비교
### 5.3 한계점 및 향후 연구

## 6. 결론 (Conclusions)
[주요 결론 요약]

## 7. 보충 자료 (Supplementary)
- Table S1: Complete DEG list
- Table S2: All enriched pathways
- Code availability: [GitHub repo]

## 8. 참고문헌 (References)
[관련 논문 및 데이터베이스]
```

## 🔬 연구 특화 기능

### 1. 재현가능성 (Reproducibility)
```yaml
# analysis_config.yml
project: "2024_transcriptome_project"
version: "1.0.0"
environment:
  R: "4.3.0"
  packages:
    - DESeq2: "1.40.0"
    - clusterProfiler: "4.8.0"
parameters:
  fdr_cutoff: 0.05
  log2fc_cutoff: 1
  min_count: 10
```

### 2. 데이터 추적성
```markdown
## Data Provenance
- Raw data: /data/raw/fastq/
- Processed: /data/processed/counts/
- Results: /results/deseq2/
- Figures: /figures/manuscript/
- Scripts: /scripts/analysis/
```

### 3. 협업 지원
```markdown
## Author Contributions
- KS: 실험 설계, 데이터 생성
- JL: 바이오인포매틱스 분석
- MP: 통계 분석 및 시각화
- All: 원고 작성 및 검토
```

## 💡 연구 보고서 작성 팁

### DO ✅
- 방법론 상세 기술 (재현 가능하도록)
- 통계적 유의성과 생물학적 의미 구분
- 원시 데이터 접근 경로 명시
- 사용한 소프트웨어 버전 기록
- 그림에 충분한 설명 제공

### DON'T ❌
- p-value만으로 중요도 판단
- 효과 크기(effect size) 무시
- 다중검정 보정 생략
- 기술적 반복과 생물학적 반복 혼동
- 부정적 결과 숨기기

## 🚀 워크플로우 통합

### 연구 분석 → 논문 작성
```bash
# 1. 분석 수행 및 보고서 생성
/분석 transcriptome "처리군 vs 대조군 RNA-seq 분석"

# 2. 그림 생성
/구현 "volcano plot과 heatmap 생성 코드"

# 3. 통계 검증
/안정화 "FDR 계산 및 multiple testing correction 검증"

# 4. 최종 보고서
/문서화 "Nature format 논문 초안 작성"
```

## 📊 품질 체크리스트

### 분석 완성도
- [ ] QC 메트릭 포함
- [ ] 통계 방법 명시
- [ ] 다중검정 보정
- [ ] 효과 크기 보고
- [ ] 원시 데이터 링크

### 시각화 품질
- [ ] 고해상도 그림 (300 dpi+)
- [ ] 색맹 친화적 팔레트
- [ ] 충분한 레이블과 범례
- [ ] 통계적 유의성 표시

### 재현가능성
- [ ] 코드 공개
- [ ] 환경 정보
- [ ] 파라미터 문서화
- [ ] 데이터 접근성