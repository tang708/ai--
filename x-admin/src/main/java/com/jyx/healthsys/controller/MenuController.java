package com.jyx.healthsys.controller;

import com.jyx.Data_unification.Unification;
import com.jyx.healthsys.entity.Menu;
import com.jyx.healthsys.service.IMenuService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author 金义雄
 * @since 2023-02-23
 */
@Tag(name = "菜单管理", description = "菜单树查询接口")
@RestController
@RequestMapping("/menu")
public class MenuController {
    @Autowired
    private IMenuService menuService;

    @Operation(summary = "获取全部菜单（树形结构）")
    @GetMapping
    public Unification<List<Menu>> getAllMenu(){
        List<Menu> menuList = menuService.getAllMenu();
        return Unification.success(menuList);
    }
}
