# AAPS 财政危机与关校计划 — 社媒舆情扫描 (Reddit + X)

- **研究日期**: 2026-09-09 (评论分数为当日快照)
- **方法**: rdt CLI (Reddit 官方 API) 对 r/AnnArbor 执行 12 次多变体搜索 (AAPS / school closure / budget deficit / teachers leaving / school board / Ann Arbor schools budget / superintendent / close schools / teachers / budget / recall / petition), 关键词过滤 + 6 个月时间窗, 去重后 22 个相关帖; 深读 10 个线程 (排除已深读的锚点帖 1warxbo)。X/Twitter 用 bird CLI 执行 12 次搜索 (AAPS school closure / Ann Arbor schools budget / Jazz Parks / Ann Arbor school board / AAPS teachers / Ann Arbor schools consolidate / AAPS superintendent / AAPS closing schools / Ann Arbor Patterson Forest Lake closure / save our schools Ann Arbor / from:slagter / AAPS budget deficit)。
- **标注规则**: 情绪/立场 vs 事实分开; 无来源的具体传闻一律标 **UNVERIFIED**。

---

## 1. Reddit 深读线程清单 (top 10, 按重要性)

| # | 线程 | URL | 分数 (快照) | 评论数 | 日期 |
|---|------|-----|------|------|------|
| 1 | The current state of AAPS from a Parent | https://reddit.com/r/AnnArbor/comments/1szyumd/ | 285↑ (发帖时290↑) | 261 | 2026-04-30 |
| 2 | Support AAPS Teachers (6/3集会) | https://reddit.com/r/AnnArbor/comments/1tw4kt7/ | 264↑ | 28 | 2026-06-03 |
| 3 | Mass AAPS teacher resignation in August | https://reddit.com/r/AnnArbor/comments/1v6dzf0/ | 248↑ | 161 | 2026-07-25 |
| 4 | AAPS (教师薪资对比帖) | https://reddit.com/r/AnnArbor/comments/1s1tv7d/ | 168↑ | 82 | 2026-03-23 |
| 5 | Ann Arbor public school teachers enter sixth month without a new contract (WSWS) | https://reddit.com/r/AnnArbor/comments/1u0nugo/ | 107↑ | 33 | 2026-06-08 |
| 6 | AAPS Teacher Contract Negotiation (学生视角) | https://reddit.com/r/AnnArbor/comments/1tc0dxu/ | 102↑ | 106 | 2026-05-13 |
| 7 | Superintendent Jazz Parks | https://reddit.com/r/AnnArbor/comments/1u125h1/ | 75↑ | 46 | 2026-06-09 |
| 8 | AAPS cost reduction proposal | https://reddit.com/r/AnnArbor/comments/1vzsrbk/ | 39↑ | 77 | 2026-08-27 |
| 9 | 混龄班传闻帖 | https://reddit.com/r/AnnArbor/comments/1v7np00/ | 33↑ | 85 | 2026-07-27 |
| 10 | AAPS teachers contract agreement, Part Deux | https://reddit.com/r/AnnArbor/comments/1w7fwcf/ | 25↑ | 53 | 2026-09-04 |

**浅扫补充线程** (未深读, 提供脉络): Trustee Don Wilkerson 辞职 (1t4fao2, 66↑, 2026-05-05); 辞职board成员寻求回归+起诉前雇主 (1uo4c4y 36↑ 2026-07-05 / 1uv01w5 25↑ 2026-07-13); AAPS teachers contract agreement 首帖 (1vxibv4, 65↑, 2026-08-24); Any teacher update yet? (1vfqiee, 43↑, 2026-08-04); School Board Candidate Forum & Voting Resources (1wavk0a, 12↑, 2026-09-08); AAPS schools closed today (天气, 1sm2wa4, 79↑, 2026-04-15)。

---

## 2. 时间线叙事 (社媒视角)

1. **2026-03** — 薪资对比帖 (1s1tv7d): 教师贴出邻区薪级表 (Chelsea/Dexter/Ypsi/Milan), 指出AAPS起薪与顶薪均落后; 评论区出现**预算透明度请愿** (Google Docs链接, 要求BOE公开完整预算, 57↑评论)。
2. **2026-04-30** — 家长长帖 (1szyumd, 本期最热): 两个孩子学校均无完整固定师资, "30%教师离职未补", 长期代课轮换; 高阶理科课由不合格实习生任教。Top评论 (121↑): "他们正在流失资深教师且无法替补"。
3. **2026-05~06** — 合同僵局白热化: 学生发帖讲述work-to-rule影响 (1tc0dxu); 6/3数百人在Earhart行政楼外集会声援教师 (1tw4kt7, MLive报道"数百人")；6/8进入"第六个月无合同" (WSWS转载, 1u0nugo)。
4. **2026-06-09** — 学监Jazz Parks专项帖 (1u125h1): 高赞评论直接点名要其辞职 (74↑); 引用a2schools.org透明度文件称其薪酬"接近50万美元/年" (30↑, **UNVERIFIED具体数额**——另有评论称25万+, 数字不一致); 批评焦点: 她出自造成记账错误的旧管理层却获提拔+创纪录薪酬包。
5. **2026-07-25** — "8月大规模辞职"帖 (1v6dzf0): 某小学可能流失12-13名教师至外区 (**UNVERIFIED**, 单一信源); 一位自称AAPS教师的评论者确认"我知道的一所小学就有11人走, 包括我自己" (32↑, 一线证言)。
6. **2026-07-27** — 混龄班传闻 (1v7np00): "AAPS 2026-27将不补离职教师, 改开混龄班以'顶满'班额" (**UNVERIFIED**——"朋友的朋友听说"级信源); 评论区部分家长称3-4年级混龄班早已存在且不算糟。
7. **2026-08-27** — 减支方案帖 (1vzsrbk): 评论者从官方slide deck读出**时间表: 关校/合并决定于今秋做出, 2027年秋季生效** (30↑, 引自官方演示文稿属半官方); 高赞评论质疑"4个月内完成关校决定是故意压缩公众发声窗口", 且"在11月选举后的lame duck期做" (21↑, 11↑)。
8. **2026-09-04** — 合同达成 (1w7fwcf): Parks邮件确认AAEA批准临时协议; 教师内部人士 (自认AAEA成员, 自称投了反对票) 透露条款: 1.5%涨薪+顶部加一级step+医保略改善, 期限存争议 (有称1年、有称回溯至2026-01的2年期, **两种说法并存, UNVERIFIED**)。Top分析帖 (39↑): "买一年劳资稳定→用卖楼回血基金余额→选举后再做关校决定→2027秋实施→再谈长约"。

---

## 3. X/Twitter 发现

X上讨论量显著小于Reddit, 且多为机构号/记者号转发, 缺乏Reddit式的一线证言层:

| 账号 | 内容 | 日期 | URL |
|------|------|------|-----|
| @MichCapCon (Michigan Capitol Confidential, 保守派) | "Ann Arbor学区因超编雇员+2020年来流失1000+学生而面临'budget challenge'" (发两遍, 9/2与9/9) | 2026-09-02 / 09-09 | https://x.com/MichCapCon/status/2097746859976458324 |
| @A2schools (官方) | 9/3 Pittsfield图书馆预算听取会公告 | 2026-09-02 | https://x.com/A2schools/status/2095242378399375368 |
| @MLive | 2.4-mill税续期助力建筑维修与长期bond项目 | 2026-08-02 | https://x.com/MLive/status/2083873468269908097 |
| @MLive | "3%的2600+名AAPS员工年薪超$10万, 仅1/10教师超$9万" | 2026-08-14 | https://x.com/MLive/status/2088225170863382838 |
| @MISheffield | "她辞职几个月后学区发现一笔造成 **$25M** 预算缺口的'文书'错误" | 2026-01-27 | https://x.com/MISheffield/status/2016168605612699809 |
| @jricole (Juan Cole, UM教授) | Tlaib背书Rima Mohammad竞选校board: "愤怒的妈妈和图书馆员最能对抗法西斯" | 2026-07-31 | https://x.com/jricole/status/2083015378503119260 |
| @OurRevolution | 背书Mohammad连任, 强调其"financial accountability"立场 | 2026-08-28 | https://x.com/OurRevolution/status/2093393927575351523 |
| @TradeUnionJake | 攻击Mohammad (10/7声明措辞+毒品政策), 显示board选举的意识形态裂痕 | 2026-08-04 | https://x.com/TradeUnionJake/status/2084656837266231431 |
| @himbopresident | 讽刺: "老年选民……会在AAPS流失100%教师时看着自己房产价值崩掉" | 2026-08-15 | https://x.com/himbopresident/status/2088748473923338481 |

**注**: bird搜索"Ann Arbor schools consolidate"“AAPS budget deficit”“Patterson/Forest Lake closure”均无结果——**X上没有流传具体校名的关校名单**, 这与Reddit一致; 校名级传闻目前不存在于公开社媒 (可能存在于封闭Facebook群组, 见@LenaKauffman提及"AAPS school closure Facebook post"但那是2024年雪天停课帖, 非关校)。前MLive教育记者@slagter (Marty Slagter) 2024年中已离任, 其账号存档了2024年$20.4M/$25M削减计划的历史脉络。

---

## 4. 综合分析

### 4.1 社区派系图谱

| 派系 | 核心主张 | 代表声音 |
|------|---------|---------|
| **问责行政派** (最大声量) | 危机根源是管理失职: Jazz Parks提拔自出错旧班子、创纪录薪酬、行政bloat; 要求Parks及部分board成员下台 | 1u125h1 (74↑辞职呼吁), 1tw4kt7 (47↑/22↑), 1w7fwcf (18↑ "remove this board, Parks, and Dawn Linden") |
| **结构性拨款派** | 根源是Prop A后州人均拨款跑输通胀+入学下降, "数学就是这么紧", 换人解决不了; 出路是countywide operating millage | 1tc0dxu (60↑/42↑), 1w7fwcf (18↑ "I think the math is just really tight") |
| **关校务实派** | "入学跌了就该关校合并、卖楼、裁冗员"——把减支方案当必要药方 | 1tw4kt7 (15↑), 1vzsrbk (11↑ "Sell those buildings... Sell Community. Consolidate programs, close buildings") |
| **反关校/程序正义派** | 不反对减支但反对仓促时间表, 认为"4个月定关校=故意压缩公众参与", 且安排在选举后lame duck | 1vzsrbk (23↑/21↑) |
| **教师工会批评派** (从左) | 指AAEA领导层 (Fred Klein) 去年12月让合同无声过期、未组织抵抗 ("demobilized"); 教师被迫work-to-rule | 1u0nugo (WSWS框架), 1tc0dxu (95↑ "他们合法不能罢工, 这是仅有的杠杆") |

注意: "责怪行政"与"责怪州拨款"两派在线程内直接交锋 (1tc0dxu 60↑ vs 后续讨论; 1w7fwcf 18↑明确反驳换人论), **总体上问责行政派在r/AnnArbor占压倒性声量**, 但高信息度评论者多持结构派立场。

### 4.2 教师一线证言 (自称身份, 按分数)

- **u/Then-Fig6479** (自称双教师家庭, 1szyumd, 65↑): "我和丈夫去附近几个区能多挣近$60K, 还不算医保省的和每天2小时通勤——我们max在step 11, 多数区现在max 13-15。住不起A2, 住35分钟外。"
- **u/A-rizzle70** (自称25年AAPS教龄, 1tw4kt7, 12↑): "唯一让学校变成shit show的是行政cabinet……board对学监想要的一切照单全收。在任board成员公开鄙视教师 (Feaster, Baskett, Schmid)。"
- **u/Various_Ad_6551** (自称离职教师, 1v6dzf0, 32↑): "一所AAPS小学11名教师正在离开, 我知道的就这些, 包括我。不只是钱——领导力、士气、工作环境都在赶人走。"
- **u/enlightenedbum2** (自称AAEA成员投反对票, 1w7fwcf, 25↑): "我们算是怂了……1.5%涨薪, 顶部加一级还远追不上邻区 (Wayne-Westland能多挣$15K)。"
- **u/TeacherPatti** (自称前AAPS现Wayne County教师, 多帖): "来Wayne County吧, 钱在这边。林肯Park明年顶到$123-125K。" (数字为传闻级, **UNVERIFIED**)
- **u/Gibder16** (1v6dzf0, 27↑): "某高中一个8人系走了4个。不是一所学校, 是所有学校。"
- **u/lemjor10** (1v7np00, 30↑, 自称住A2在外区任教): "AAPS行政严重bloat, bloat的行政为证明存在感不停骚扰教师、搞出荒谬流程。"

### 4.3 家长/社区行动盘点

| 行动 | 状态 | 证据 |
|------|------|------|
| **预算透明度请愿** (要求BOE公开完整预算) | 2026-03活跃 | 1s1tv7d 顶评57↑附Google Docs链接 |
| **6/3教师声援集会** (Earhart楼, 数百人) | 已发生 | 1tw4kt7 + MLive报道链接 |
| **board会议公众发言** | 持续, 学生/教师/家长均参与; 有评论称board"像鱼缸里的鱼一样瞪着你"无回应 (24↑) | 1szyumd, 1tc0dxu (107↑建议学生组团发言上MLive) |
| **2026-11 board选举** | 8人竞4席+2人竞部分任期; 9/17候选人论坛; Tlaib/Our Revolution背书Mohammad, 右翼账号攻击她——选举已成危机公投 | 1wavk0a, 1vzsrbk (26↑ "leadership change", 11↑ "lame duck后全被炒"), X多条 |
| **正式recall运动** | **未发现** — r/AnnArbor搜"recall"无任何针对AAPS board的recall帖 (仅有市议会旧闻); 不满能量全部导向11月选举而非recall | r11搜索结果 |
| **转学潮** | 多条传闻级评论指向私立/邻区/ homeschool (homeschool 4%→6% post-pandemic, 引研究); "rock and hard place"死亡螺旋叙事 (8↑) | 1tc0dxu (15↑/8↑), 1v7np00 |

### 4.4 对学监Jazz Parks的舆情温度

- 6/9专项帖内top评论即辞职呼吁 (74↑); "Never should have given her the job——她来自那个不小心超支数百万的旧管理团队, 却得到提拔加薪" (64↑)。
- 薪酬争议: 官方透明度文件被引用, 但社媒数字混乱——"刚低于50万/年" (30↑) vs "超25万/年" (41↑) vs "30万左右" (**具体数额UNVERIFIED, 区间$250K-$500K**)。
- 8/27减支方案被讥为"一次性输血, 一大块还要喂给bloat行政盖新楼" (41↑, 指迁入Dixboro Rd新行政楼)。

---

## 5. 官方未确认、社媒流传的传闻清单 (全部 UNVERIFIED)

1. **[UNVERIFIED] 混龄班顶班额**: "AAPS 2026-27不补离职教师, 改设多年级混龄班以把班额顶到上限" (1v7np00, 2026-07-27, 三手信源; 官方未确认; 评论区称部分混龄班历史上一直存在, 削弱了传闻独特性)。
2. **[UNVERIFIED] 单校12-13名教师8月出走**: 某AAPS小学 (未点名) 可能一夜失去12-13名教师, 且"尚未正式通知因为要保住医保到新岗位开始" (1v6dzf0, 2026-07-25); 自称教师者确认另一数字"11人含本人"。无官方离职统计发布。
3. **[UNVERIFIED] $25M vs $14M缺口数字分歧**: X上流传"文书错误造成 **$25M** 预算缺口" (@MISheffield, 2026-01-27), 与官方渠道的$14M记账错误说法不一致——社媒把不同口径的数字混用放大。
4. **[UNVERIFIED] 学监薪酬"近$50万/年"**: 引自a2schools.org透明度PDF但与"25万+"说法冲突, 数字未核实。
5. **[UNVERIFIED] 关校时间表解读**: "关校合并今秋决定、2027秋生效"来自官方slide deck (半官方); 但"board故意安排在11月选举后的lame duck期敲定以规避选民惩罚"是社媒推断, 无官方确认 (1vzsrbk, 21↑/11↑)。
6. **[UNVERIFIED] "1年vs 2年"新教师合同期限**: 9/4协议达成后, 社媒同时流传"仅1年" (支撑"买稳定→选举后关校→再谈判"阴谋论, 39↑) 与"回溯至2026-01的2年期、2027年3月开始新一轮谈判" (7↑) 两种说法。
7. **[未发现] 具体关校名单**: **Reddit和X公开层面均未流传点名学校的关校名单** (Patterson/Forest Lake等校名搜索零结果)。锚点背景中的"关2-6校"范围在社媒仅以泛称出现; 点名讨论仅限个别评论者自己的建议 (如"Sell Community [High]"), 非传闻名单。名单级讨论若存在, 更可能在封闭Facebook家长群内 (无法从公开CLI访问)。
8. **[UNVERIFIED] 邻区薪资数字**: Lincoln Park顶薪"$123K-125K明年"、Brighton起薪$52,211等为社媒用户手贴, 方向与官方薪资表一致但未逐项核实 (1v7np00, 57↑)。

---

## 6. 方法与局限

- 评论分数为2026-09-09快照; rdt search对宽泛查询召回偏弱, 已用12个变体+关键词后滤缓解。
- bird无Twitter登录cookie (Safari EPERM), 走匿名搜索通道, 结果偏机构号; X端讨论密度本身也确实低于Reddit, 教师一线证言几乎全部来自Reddit。
- 封闭Facebook群组 (家长组织主阵地, 多条Reddit/X评论间接提及) 不可达, 是本扫描最大盲区。
- 排除锚点帖1warxbo ('Please help me understand AAPS', 87↑61评, 2026-09-08)——已由前置任务深读。
