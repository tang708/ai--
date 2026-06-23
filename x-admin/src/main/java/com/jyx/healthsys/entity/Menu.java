package com.jyx.healthsys.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonInclude;

import io.swagger.v3.oas.annotations.media.Schema;

import lombok.Data;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <p>
 *
 * </p>
 *
 * @author 金义雄
 * @since 2023-02-23
 */
@Schema(description = "菜单实体")
@Data
@TableName("j_menu")
public class Menu implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "菜单ID")
    @TableId(value = "menu_id", type = IdType.AUTO)
    private Integer menuId;

    @Schema(description = "前端组件路径")
    private String component;

    @Schema(description = "路由路径")
    private String path;

    @Schema(description = "重定向路径")
    private String redirect;

    @Schema(description = "路由名称")
    private String name;

    @Schema(description = "菜单标题")
    private String title;

    @Schema(description = "图标")
    private String icon;

    @Schema(description = "父菜单ID")
    private Integer parentId;

    @Schema(description = "是否叶子节点")
    private String isLeaf;

    @Schema(description = "是否隐藏")
    private Boolean hidden;

    @Schema(description = "子菜单列表（非数据库字段）")
    @TableField(exist = false)
    @JsonInclude(JsonInclude.Include.NON_EMPTY)
    private List<Menu> children;

    @Schema(description = "元数据（非数据库字段）")
    @TableField(exist = false)
    private Map<String,Object> meta;
    public Map<String,Object> getMeta(){
        meta = new HashMap<>();
        meta.put("title",title);
        meta.put("icon",icon);
        return meta;
    }


}
