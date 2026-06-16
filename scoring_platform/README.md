# 评分系统占位说明

评分系统是未来第三个独立系统，目前仅保留边界说明，不实现具体评分协议。

## 目标边界

- 只读 `question_bank/`。
- 只读 `student_attempts/`。
- 写入 `grading_results/`。
- 不调用出题系统 Web。
- 不调用学生系统 Web。

## 未来输入

```text
question_bank/
student_attempts/
```

## 未来输出

```text
grading_results/
```

## 暂不固定的内容

- `student_attempts/` 的最终 JSON schema。
- 写作和口语评分 rubrics。
- 评分结果 `result.json` 的最终字段。
- 人工复核或多次评分的合并策略。

## 建议实现顺序

1. 等学生系统的单项练习和作答保存稳定。
2. 先支持听力/阅读客观题评分。
3. 再支持写作评分。
4. 最后支持口语评分和套卷总评。
