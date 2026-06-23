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
import java.util.List;

/**
 * <p>
 *
 * </p>
 *
 * @author 金义雄
 * @since 2023-02-23
 */
@Schema(description = "用户实体")
@Data
@AllArgsConstructor
@NoArgsConstructor
@TableName("j_user")
public class User implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "用户ID")
    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;

    @Schema(description = "用户名")
    private String username;

    @Schema(description = "密码")
    private String password;

    @Schema(description = "邮箱")
    private String email;

    @Schema(description = "手机号")
    private String phone;

    @Schema(description = "状态：1启用 0禁用")
    private Integer status;

    @Schema(description = "头像URL")
    private String avatar;

    @Schema(description = "逻辑删除：1已删除 0未删除")
    private Integer deleted;

    @Schema(description = "角色ID列表（非数据库字段）")
    @TableField(exist = false)
    private List<Integer> roleIdList;

    @Schema(description = "新密码（修改密码时使用，非数据库字段）")
    @TableField(exist = false)
    private String newPassword;

}
