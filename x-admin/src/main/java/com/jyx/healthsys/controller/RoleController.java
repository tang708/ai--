package com.jyx.healthsys.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.jyx.Data_unification.Unification;
import com.jyx.healthsys.entity.Role;
import com.jyx.healthsys.entity.User;
import com.jyx.healthsys.service.IRoleService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author 金义雄
 * @since 2023-02-23
 */

@Tag(name = "角色管理", description = "角色CRUD及列表查询接口")
@RestController
@RequestMapping("/role")
public class RoleController {
    @Autowired
    private IRoleService roleService;

    @Operation(summary = "分页获取角色列表")
    @GetMapping("/list")
    public Unification<Map<String,Object>> getRoleList(
            @Parameter(description = "角色名称（可选筛选）") @RequestParam(value = "roleName", required = false) String roleName,
            @Parameter(description = "当前页码") @RequestParam(value = "pageNo") Long pageNo,
            @Parameter(description = "每页条数") @RequestParam(value = "pageSize") Long pageSize) {

        LambdaQueryWrapper<Role> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(StringUtils.hasLength(roleName), Role::getRoleName, roleName);
        wrapper.orderByDesc(Role::getRoleId);

        Page<Role> page = new Page<>(pageNo, pageSize);
        roleService.page(page, wrapper);

        Map<String, Object> data = new HashMap<>();
        data.put("total", page.getTotal());
        data.put("rows", page.getRecords());
        return Unification.success(data);
    }


    @Operation(summary = "新增角色")
    @PostMapping
    public Unification<?> addRole(@RequestBody Role role){
        boolean result = roleService.addRole(role);
        if (result) {
            return Unification.success("新增成功");
        } else {
            return Unification.fail("用户名已存在");
        }
    }

    @Operation(summary = "修改角色信息")
    @PutMapping
    public Unification<?> updateRole(@RequestBody Role role){
        roleService.updateRole(role);
        return Unification.success("修改成功");
    }

    @Operation(summary = "根据ID获取角色详情")
    @GetMapping("/{id}")
    public Unification<Role> getRoleById(
            @Parameter(description = "角色ID") @PathVariable("id") Integer id){
        Role role = roleService.getRoleById(id);
        return Unification.success(role);
    }

    @Operation(summary = "根据ID删除角色")
    @DeleteMapping("/{id}")
    public Unification<Role> deleteRoleById(
            @Parameter(description = "角色ID") @PathVariable("id") Integer id){
        roleService.deleteRoleById(id);
        return  Unification.success("删除成功");
    }

    @Operation(summary = "获取全部角色列表")
    @GetMapping("/all")
    public Unification<List<Role>> getAllRole(){
        List<Role> roleList = roleService.list();
        return Unification.success(roleList);
    }


}
