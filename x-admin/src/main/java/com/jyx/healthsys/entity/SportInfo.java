package com.jyx.healthsys.entity;


import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Schema(description = "运动知识实体")
@Data
@TableName("sport_info")
@NoArgsConstructor
@AllArgsConstructor
public class SportInfo implements Serializable {

    @Schema(description = "运动知识ID")
    @TableId(type = IdType.AUTO)
    @TableField(value = "id")
    private Integer id;

    @Schema(description = "运动类型")
    @TableField(value = "sport_type")
    private String sportType;

    @Schema(description = "适宜时间")
    @TableField(value = "suitable_time")
    private String suitableTime;

    @Schema(description = "适宜心率")
    @TableField(value = "suitable_heart_rate")
    private String suitableHeartRate;

    @Schema(description = "适宜频率")
    @TableField(value = "suitable_frequency")
    private String suitableFrequency;

    @Schema(description = "推荐速度")
    @TableField(value = "recommended_speed")
    private String recommendedSpeed;

}
