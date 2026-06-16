-----------------------------------
  今回の更新
-----------------------------------

精英=220
种族=314
种族2=319

-----------------------------------
  重新实装精英部下
-----------------------------------
MONSTER_SKILL.ERB
DUNGEON_BATLLE2.ERB
DUNGEON_BATTLE.ERB
MONSTER_DATA.ERB
LVUP.ERB
LOOK.ERB
CHAR_MAKE.ERB
SHOP_MONSTER.ERB
SHOP.ERB
_DRAW_MAINMENU.ERB

◆精英部下的技能
DUNGEON_BATLLE2.ERB>
	@DUEL_ATTACK>
		668行> 添加调用@SLAVE_MONSTER_SKILL
MONSTER_SKILL.ERB>
	添加函数@SLAVE_MONSTER_SKILL
	添加函数@USE_MONSTER_SKILL
	

◆修复对种族2的先手计算
DUNGEON_BATTLE.ERB>
	@SPEED_PLUS> 添加518~598


◆MONSTER_DATA
MONSTER_DATA.ERB>
	@MONSTER_DATA> 
		添加修改263~327

◆等级提升计算
LVUP.ERB>
	@LVUP> 添加8~14

◆精英部下的外观
LOOK.ERB>
	@LOOK_SET
		!$RACE之后
	@LOOK_INFO
		添加903~923
		修改926附近
		修改1037~1058

◆精英的生成素质
CHAR_MAKE.ERB>
	133>199>452>579>592~607>613>
	627~644>654>664>690>
		修改基础素质
	@SET_CHAR_CLOTH>
		3201~3277> 精英服装与装备

◆召唤精英部下界面
添加SHOP_MONSTER.ERB
SHOP.ERB>
	@USERSHOP
	156> 添加输入
_DRAW_MAINMENU.ERB>
	>添加按钮



-----------------------------------
  主角改名
-----------------------------------
CHARA_NAME_EDIT.ERB
修改@CHARA_INFO_NAME_EDIT
添加@CHARA_INFO_SELFNAME_EDI



-----------------------------------
  人物信息
-----------------------------------
CHAR_INFO.ERB
CHAR_INFO_SHOW.ERB
CHAR_INFO_SHOW_TALENT.ERB

◆重写了人物列表
@SHOW_CHARA_INFO_LIST

◆人物信息分页
@CHARA_INFO_INDIVIDUAL

◆信息页调整并增加内容
@SHOW_CHARA_INFO

◆新增人物的素质达成信息
CHAR_INFO_SHOW_TALENT.ERB


-----------------------

-----------------------


◆

◇◇

◆