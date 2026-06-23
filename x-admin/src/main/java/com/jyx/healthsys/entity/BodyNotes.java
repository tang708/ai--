package com.jyx.healthsys.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Schema(description = "身体信息历史记录实体")
@Data
@AllArgsConstructor
@NoArgsConstructor
@TableName("j_body_notes")
public class BodyNotes {

    private static final long serialVersionUID = 1L;

    @Schema(description = "用户ID")
    @TableField(value = "id")
    private Integer id;

    @Schema(description = "历史记录ID")
    @TableId(value = "notes_id", type = IdType.AUTO)
    private Integer notesid;

    @Schema(description = "姓名")
    private String name;

    @Schema(description = "年龄")
    private Integer age;

    @Schema(description = "性别")
    private String gender;

    @Schema(description = "身高(cm)")
    private Double height;

    @Schema(description = "体重(kg)")
    private Double weight;

    @Schema(description = "血糖(mmol/L)")
    @TableField(value = "bloodSugar")
    private Double bloodSugar;

    @Schema(description = "血压(mmHg)")
    @TableField(value = "bloodPressure")
    private String bloodPressure;

    @Schema(description = "血脂(mmol/L)")
    @TableField(value = "bloodLipid")
    private String bloodLipid;

    @Schema(description = "心率(次/分)")
    @TableField("heart_rate")
    private double heartRate;

    @Schema(description = "视力")
    @TableField("vision")
    private Integer vision;

    @Schema(description = "睡眠时长(小时)")
    @TableField("sleep_duration")
    private double sleepDuration;

    @Schema(description = "睡眠质量")
    @TableField("sleep_quality")
    private String sleepQuality;

    @Schema(description = "是否吸烟")
    @TableField("smoking")
    private boolean smoking;

    @Schema(description = "是否饮酒")
    @TableField("drinking")
    private boolean drinking;

    @Schema(description = "是否运动")
    @TableField("exercise")
    private boolean exercise;

    @Schema(description = "饮食类型")
    @TableField("food_types")
    private String foodTypes;

    @Schema(description = "饮水量(ml)")
    @TableField("water_consumption")
    private double waterConsumption;

    @Schema(description = "记录日期")
    @TableField("Date")
    private Date Date;

}
