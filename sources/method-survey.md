# 用ACS tract级数据做学区入学需求预测/关校分析:方法学与数据管道先例调研

**日期**: 2026-09-09 · **用途**: AAPS(Ann Arbor Public Schools)入学需求预测与关校情景分析的方法选型
**数据锚点(已确认)**: Census Reporter API (`api.censusreporter.org`) 免key可用;ACS 5yr B01001(分年龄性别);AAPS为密州unified学区,覆盖Ann Arbor市+8个镇区约125平方英里。

---

## 0. 背景锚点(本地事实)

- AAPS 2025秋季注册年报告: 较2024秋再降1.17%(-196人),自2013-14累计仍净增176人,但2019后趋势线(dashed)向下;COVID后降幅放缓。
  - https://resources.finalsite.net/images/v1766076279/a2schoolsorg/edqsqq2k8385257scmr7/2025StudentEnrollmentAnnualReport12172025.pdf
- Ann Arbor Observer: "Day of Reckoning Nears for AAPS" — 至少2所、至多6所学校可能关闭。
  - https://annarborobserver.com/day-of-reckoning-nears-for-aaps/
- Plante Moran法证审计(2024-06): 支出未随入学下降而收缩。
  - https://resources.finalsite.net/images/v1729708257/a2schoolsorg/ih4y684ui17l69e8ukgt/PlanteMoranForensicReport-AAPS.pdf
- SEMCOG 2050学区学龄人口预测: 2020-2035区域内所有ISD(含Washtenaw)学龄人口继续下降 — 独立于本项目的宏观先行指标,可作对照/校准。
  - https://www.semcog.org/wp-content/uploads/2025/08/Quick-Facts_2050-Forecast-of-SchoolAge-Population.pdf

---

## 1. 入学预测方法学先例

### 1.1 Cohort survival / grade progression ratio(队列推进法)— 行业标准

**原理**: 用历史"年级g第t年 → 年级g+1第t+1年"的存活比率推进在读学生;入年级(K)由外部外生给定——最常用**出生数滞后法**(K入学年 ≈ 出生年+5,乘以tract级"出生→注册"捕获率)。

具体先例:
- **MSBA(马州学校建设管理局)方法论** — modified grade-to-grade cohort survival,是学区设施规划的事实标准参考:
  - http://www.massschoolbuildings.org/building/prerequisites/enrollment_methodology
- **FutureThink给WJCC学区的报告(2016)** — 最清晰的教学式说明:cohort survival + 出生数据 + housing development叠加:
  - https://wjccschools.org/redistricting/wp-content/uploads/sites/34/2017/09/Enrollment-Report-FutureThink-November-15-2016.pdf
- **Arlington Public Schools年度10年预测(2022与2026版)** — 公立学区自查范本: 出生数外推→K入口→队列推进,PreK单独处理:
  - https://www.apsva.us/wp-content/uploads/2022/12/APS-Fall-2022-10-Year-Enrollment-Projections.pdf
  - https://www.apsva.us/wp-content/uploads/sites/57/2026/01/2026.01.13-2025-Fall-Projections-Report-FINAL.pdf
- **Cooper Center(弗吉尼亚州级)2024方法论** — 州级K-12预测的公开方法论文档:
  - https://www.coopercenter.org/sites/default/files/2025-01/SchoolEnrollmentProjections_Methodology_2024-01-16.pdf
- **DC OSSE 2025 MFP附录** — 两阶段(全市→学校)预测方法:
  - https://dme.dc.gov/sites/default/files/dc/sites/dme/publication/attachments/2025%20MFP%20Annual%20Supplement%20Appendix%204_0.pdf

### 1.2 Housing-driven预测(开发量驱动)

咨询公司(FLO Analytics、MGT、Applied Economics等)的标准做法: 在cohort survival基线上叠加"已知住宅开发管道×每户学生产出系数(student yield per unit,按住宅类型分层)"。

- **FLO Analytics方法说明页** + 各学区公开报告(结构相同: 历史注册→出生趋势→开发管道→按校预测):
  - https://flo-analytics.com/expertise/what-we-do/enrollment-forecasting
  - https://flo-analytics.com/about/news-insights/student-enrollment-forecasting-explained-0
  - Bend-La Pine 2026-27~2035-36: https://resources.finalsite.net/images/v1780339028/bendk12orus/i7nmgfvttvivs3d9ilmo/BLS2026-27to2035-36EnrollmentForecastsReportFinal.pdf
  - Beaverton 2023-2032: https://resources.finalsite.net/images/v1715996265/beavertonk12orus/kshh3pso0cyhtdwvct0i/FLO_BSD_Forecast_2023_to_2032.pdf
  - Bellingham 2026-27~2035-36: https://resources.finalsite.net/images/v1773177601/bellinghamschoolsorg/eqtsutgn71pducwpbkey/BellinghamSD2026-27to2035-36EnrollmentForecastsReport1.pdf
- **MGT给Madison Metro SD(威州,大学城,与Ann Arbor最相似的对照)**: 
  - https://resources.finalsite.net/images/v1777993996/madisonk12wius/g2j7realbn7va0oin0nj/SY2526StudentForecastReport_MadisonMetroSD4.pdf
- **Applied Economics给Cache County SD**: 
  - https://resources.finalsite.net/images/v1754947770/ccsdutorg/pwyixguumbnj6n2fnlna/AE_CacheReport_FinalSY25.pdf

**要点**: Ann Arbor开发管道数据可从市规划部门(major projects list)获取;大学城还需考虑大学附属住房的极低student yield——这是AAPS特有的修正项。

### 1.3 边界叠加方法(tract人口 → attendance boundary内学龄人口)

三档精度,误差递减:

| 方法 | 原理 | 适用/局限 |
|---|---|---|
| **Areal weighting(面积加权)** | 按tract∩boundary面积比例分摊人口 | 实现最简单(tobler一行);在人口分布不均的tract(如含公园/商业区/机场)偏差大 |
| **Dasymetric mapping(分区密度)** | 用辅助面(NLCD土地覆盖: 只在developed/residential像元内分摊)或掩膜重分配 | PySAL `tobler` 内置`binary_dasymetric`/`masked_area_interpolate`,直接支持栅格;文献上是小面积插值精度提升的标准做法 |
| **Block-level分配** | ACS不发布block级,但**十年普查(2010/2020 Decennial)有block级年龄×性别**;用block做原子单位,把2020 block人口按其centroid/面积主体归入boundary,再把tract级ACS特征按block占比下推 | 精度最高;SABINS和Bardelli管道都用block做原子;注意ACS特征仍来自tract(block只有粗年龄结构) |

工具与文献:
- **tobler(PySAL)— areal interpolation专用库**: `area_interpolate`, `binary_dasymetric`(NHGIS-like方法), `masked_area_interpolate`(任意栅格掩膜):
  - https://pysal.org/tobler/dev/user-guide/binary_dasymetric.html
  - https://github.com/pysal/tobler
- **SABINS(School Attendance Boundary Information System)** — NSF资助的K-12边界+人口数据基础设施,方法论文公开(如何把census数据接到边界上):
  - 项目页: https://www.nhgis.org/sabins-school-areas
  - 方法论文: https://pmc.ncbi.nlm.nih.gov/articles/PMC5693243/
  - 数据设计codebook: https://assets.ipums.org/_files/nhgis/sabins/sabins_database_design_codebook.pdf
- **EdWorkingPapers 2023(校级特征估算新法)** — 用学校位置推算catchment再聚合census数据,与boundary法互为校验:
  - https://edworkingpapers.com/ai23-804
- **Bipartite graph方法处理"不可通约空间分区"(学校-社区)** — 学术方法参考:
  - https://doi.org/10.21203/rs.3.rs-3894643/v1

---

## 2. Tract边界跨年变化: 2010 vs 2020

**问题**: ACS 5yr release的tract底图随十年普查切换——2019及以前5yr用2010 tract,2020及以后用2020 tract;Washtenaw县2020 tract有拆分/合并,直接拼接会产生假跳变。

**解法(标准做法)**: NHGIS geocrosswalk。

- **NHGIS Geographic Crosswalks主文档**: 
  - https://www.nhgis.org/geographic-crosswalks
- 要点(自官方文档):
  - 提供 **2010→2020** 与 **2020→2010** 双向tract crosswalk(源/目标含block、block group、tract);
  - 与Census Bureau官方Relationship Files不同,NHGIS权重基于**更精细模型**(block级特征派生的插值权重,可选population/housing unit/area等权重),即"每行给出源zone特征分配到目标zone的比例";
  - 官方明确建议: **从最低可用层级(block)开始构建**再聚合到tract,精度最高;
  - 对2011/2012/2014/2015/2022等非普查年也提供block group/tract crosswalk(用于ACS逐年release间的底图微调);
  - 可通过NHGIS API下载(免费账号)。
- **nhgisxwalk(R包,IPUMS官方)** — 程序化生成temporal crosswalk("atoms"法):
  - https://github.com/ipums/nhgisxwalk
- IPUMS论坛实操问答(权重怎么乘):
  - https://forum.ipums.org/t/crosswalk-between-2010-and-2020-census-tracts/6300
  - https://forum.ipums.org/t/2010-2020-tract-geographic-crosswalk/4795

**对AAPS管道的落地建议**: 用NHGIS **2010→2020 tract crosswalk(人口权重)** 把2010-2019 ACS 5yr(2010 tract)全部标准化到2020 tract;或反向统一到2010 tract再映射到边界。另一条免费路径: NHGIS还提供**已做地理标准化的时间序列表(geographically standardized time series)**,直接免掉自己拼crosswalk。

---

## 3. ACS 5yr逐年release做时间序列的注意事项

来源(均为Census Bureau官方):
- **Comparing ACS Data(官方对照规则页)**: 
  - https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data.html
- **ACS General Handbook Ch.3(单年/多年估计的理解)**: 
  - https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_general_handbook_2020_ch03.pdf
- **Ch.4(比较与MOE运算)**: 
  - https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_general_handbook_2020_ch04.pdf
- **Period Estimates博客(为什么5yr不是"平均")**: 
  - https://www.census.gov/newsroom/blogs/random-samplings/2022/03/period-estimates-american-community-survey.html

硬规则:
1. **重叠窗口不可当独立样本比较**: 如2015-2019 vs 2016-2020共享4年数据,差异的大部分是噪声共享;官方规则是**只用不重叠窗口**(2011-2015 vs 2016-2020 vs 2021-2025)做"变化"论断。逐年5yr序列只能当平滑趋势看,不能做显著性检验。
2. **MOE必须传播**: tract级B01001单岁年龄组MOE很大;求和年龄组的MOE需按官方公式(SE=MOE/1.645, 和的SE=√(ΣSE²)当独立时——但ACS同一表的年龄组相关,官方建议保守处理)。Census Reporter API直接返回error字段,照用即可。
3. **人口总量用Decennial/Population Estimates,特征分布用ACS**(官方明确建议): 2020 block/tract的学龄人口总数用2020 Census;ACS只用来拿tract级年龄结构、住房、家庭特征。
4. **2020年1yr为实验性估计**(不可比),5yr不受影响但2020版(2016-2020)受COVID数据采集影响,解读时标注。
5. tract级单年5yr样本量小→趋势建议以**3个不重叠5yr窗口**(2011-15, 2016-20, 2021-25)为主轴,中间年份仅作平滑参考。

---

## 4. 学校attendance boundary数据源

| 源 | 覆盖 | 状态 | 对AAPS可用性 |
|---|---|---|---|
| **AAPS自公布** | 本区小学/初中/高中boundary图+街道目录 | 活跃维护 | **首选**: 但官网注明"approximation of boundaries",非GIS下载件;需要从其交互地图(推测为Google/ArcGIS embed)抓GeoJSON,或向学区索取shapefile(PA请求也可) |
| **NCES EDGE SABS** | 全国,2013-14与2015-16两波 | **实验性、已停止**;覆盖不全(需查AAPS是否在2015-16波中) | 只适合做历史对照/边界变化研究,不能反映AAPS近年调整 |
| **SABINS(NHGIS)** | 2009-2013学年为主的K-12边界+预挂census数据 | 存档项目(NSF),数据仍在NHGIS分发 | 历史基线有用(边界变迁分析) |
| **EDGE district/school边界** | 学区边界(非attendance)每年更新 | 活跃(ArcGIS REST可直接拉) | 用于裁剪AAPS全域: https://nces.ed.gov/programs/edge/Geographic/DistrictBoundaries |

链接:
- AAPS attendance boundaries(入口页): https://www.a2schools.org/about-aaps/our-schools/attendance-boundaries
- AAPS街道目录(校验用): https://www.a2schools.org/about-aaps/attendance-area-by-street-directory
- SABS主页+FAQ: https://nces.ed.gov/programs/edge/sabs · https://nces.ed.gov/programs/edge/SABS/FAQs
- SABS 2015-16技术文档: https://nces.ed.gov/programs/edge/docs/EDGE_SABS_2015_2016_TECHDOC.pdf
- SABS 2015-16开放数据(ArcGIS Hub,可下载GeoJSON): https://data-nces.opendata.arcgis.com/datasets/nces::school-attendance-boundary-survey-2015-2016/about
- SABINS: https://www.nhgis.org/sabins-school-areas

**结论**: 全国性current数据源已断档(SABS停更),**AAPS自公布地图数字化是唯一现实路径**;SABS/SABINS仅作历史对照。务必用街道目录抽查数字化边界的准确性。

---

## 5. 开源先例(博客/GitHub/包)

按相关度排序:

1. **enrollcast(R包, localopen, 2026)** — cohort survival/grade progression ratio的矩阵投影实现,任意聚合层级(校/区/市),K外生给定——与推荐方法完全同构,可直接借用或Python重写:
   - https://github.com/localopen/enrollcast · 文档: https://rorylawless.r-universe.dev/enrollcast/doc/manual.html
2. **Emanuele Bardelli《On Redrawing School Attendance Boundaries》(2025-03博客)** — **与本任务最接近的端到端先例**: 学区因入学下降关校并重画边界,作者建了DuckDB+spatial扩展的GIS管道(census block为原子、学生geocode、ST_Contains空间连接、GeoJSON聚合、实时边界方案影响投影,用于公众会议)。工具后来开源:
   - https://ebardelli.com/posts/redrawing-school-attendance-boundaries/
3. **dssg/predicting_student_enrollment_public** — DSSG对芝加哥公立学校的校级注册预测(统计模型,公开代码):
   - https://github.com/dssg/predicting_student_enrollment_public
4. **mlchrzan/Deeper-Roots + EdWorkingPapers论文** — ML提前5年预测学区大规模关校(≥10%学校),用NCES管理数据2000-2018——"关校预测"侧的先例:
   - https://github.com/mlchrzan/Deeper-Roots · https://edworkingpapers.com/sites/default/files/ai25-1210.pdf
5. **charlie2bored/nyc-d2-enrollment-forecasting** — NYC 30所小学的回测预测管道(分析师边界 vs 模型):
   - https://github.com/charlie2bored/nyc-d2-enrollment-forecasting
6. **zeroclutch/emptyschools** — 圣何塞关校的人口趋势调查:
   - https://github.com/zeroclutch/emptyschools
7. **sdpclosures.org(费城关校分析)** — 成品分析网站,两波关校的驱动因素对比:
   - https://sdpclosures.org/
8. **anna-ringwood/atlanta-public-schools-closures** — CMU GIS课程项目,APS关校影响分析:
   - https://github.com/anna-ringwood/atlanta-public-schools-closures
9. **tobler(PySAL)** — 面积加权/二值dasymetric/栅格掩膜插值的现成实现(见§1.3)。
10. **pygris / tidycensus** — Census几何+数据的取数层(pygris免key可下TIGER几何;tidycensus走官方API需key):
    - https://walker-data.com/pygris/ · https://walker-data.com/tidycensus/articles/spatial-data.html

---

## 6. 推荐方案排序

### 推荐1(主方案): 双轨 = 校级cohort survival(主) + tract-B01001人口结构外推(校准/情景)
1. **取数**: AAPS历史分年级分校注册(mischooldata.org + AAPS年报,2002-03起可得)→ 校级grade-by-year矩阵。
2. **主预测**: cohort survival / grade progression ratio(enrollcast同构;3-5年历史比率取均值/加权,K入口外生)。K入口 = Washtenaw县/AAPS域内出生数滞后5年 × 捕获率;出生数用NCHS/Michigan DHHHS Vital Records按居住地统计,AAPS域内可按boundary内tract权重近似。
3. **人口结构轨**: Census Reporter API拉B01001(及B01001细分单岁表B01001_001族与年龄桶),按§2的NHGIS crosswalk统一到2020 tract;三个不重叠5yr窗口(2011-15/2016-20/2021-25)建立趋势;boundary内学龄(5-9/10-14岁)人口用**2020 Decennial block级**做block-level分配(推荐3档中的最高档),ACS tract特征按block占比下推。
4. **对齐**: 两轨互相校验——boundary内学龄人口变化率 vs 该校历史注册变化率,差异即"捕获率/择校流出(private/charter/choice)"信号,用AAPS年报的schools-of-choice数据修正。
5. **情景**: 关校情景即boundary重组——按Bardelli模式用block原子重聚合,输出各情景下校容量利用率;对照SEMCOG区域预测作宏观 sanity check。

### 推荐2(简化起步): 纯tract人口结构轨
只用ACS/Decennial tract-block数据推boundary内学龄人口,隐含"捕获率恒定"假设。优点: 全免key、一周可跑通;缺点: 忽略choice/private流出与年级结构动态,只适合初筛"哪些学校的人口基本面最弱"。

### 推荐3(补充): housing-driven叠加
拿到Ann Arbor市major projects/permit数据后,叠加student yield per unit(FLO报告有可引用系数区间),修正增长区预测。适合作为推荐1的敏感性分析而非主干。

### 明确不推荐
- 把逐年ACS 5yr当独立样本做回归/显著性检验(违反§3规则1);
- 纯areal weighting直接tract→boundary(Ann Arbor含大量非居住用地: 校园、公园、商业区,dasymetric/block级提升明显);
- 依赖SABS/SABINS做current边界(已停更,2015-16为最新)。

---

## 附: 关键技术操作备忘
- Census Reporter API: `https://api.censusreporter.org/1.0/data/show/latest?table_ids=B01001&geo_ids=050|040` 系列;tract级 `06000US26161...` (Washtenaw county=26161)。
- NHGIS crosswalk免费但需注册账号(或用API key);`nhgisxwalk`(R)可程序化生成。
- pygris取2020 tract TIGER几何免key;叠加用geopandas overlay或DuckDB spatial(Bardelli路线,对公众演示友好)。
- MOE: Census Reporter返回的error字段 → SE=error/1.645;年龄组求和按Ch.4公式传播。

*所有URL于2026-09-09访问/检索。置信度: 方法论与官方规则=高(多源官方文档);开源先例=直接验证仓库/博客存在;AAPS本地数字引自学区/Observer/SEMCOG原始文件。*
