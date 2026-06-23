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

@Schema(description = "病情运动详情实体")
@Data
@AllArgsConstructor
@NoArgsConstructor
@TableName("detail")
public class Detail implements Serializable {

    @Schema(description = "详情ID")
    @TableId(type = IdType.AUTO)
    @TableField(value = "id")
    private Integer id;

    @Schema(description = "运动类型")
    @TableField("sport_type")
    private String sportType;

    @Schema(description = "关联疾病")
    private String disease;

    @Schema(description = "锻炼方法")
    private String method;

    @Schema(description = "注意事项")
    private String notes;

}
