local mapinfo = {
	name        = "KForge Map",
	shortname   = "kforge",
	description = "KForge Zero-K draft export",
	author      = "KForge",
	version     = "v0.1",
	modtype     = 3,

	maphardness     = 140,
	notDeformable   = false,
	gravity         = 130,
	tidalStrength   = 18,
	maxMetal        = 1.20,
	extractorRadius = 110,
	voidWater       = false,
	autoShowMetal   = true,

	smf = {
		minheight = -128,
		maxheight = 384,
		mapfile = "maps/kforge.smf",
		metalmapTex = "kforge_metalmap.tga",
		typemapTex = "kforge_typemap.tga",
	},

	resources = {
		splatDistrTex = "kforge_splatmap.tga",
		splatDetailNormalTex = {
			"grass.tga",
			"rock.tga",
			"sand.tga",
			"snow.tga",
			alpha = true,
		},
	},

	splats = {
		texScales = {0.00471, 0.00097, 0.0013, 0.0027},
		texMults  = {0.5, 0.31, 0.5, 0.65},
	},

	teams = {
		[0] = {startPos = {x = 280.42, z = 281.93}},
		[1] = {startPos = {x = 249.29, z = 243.5}},
		[2] = {startPos = {x = 248.45, z = 246.33}},
		[3] = {startPos = {x = 251.4, z = 242.31}},
		[4] = {startPos = {x = 251.8, z = 243.0}},
	},

	terrainTypes = {
		[0] = { name = "Default", hardness = 1.0, receiveTracks = true, moveSpeeds = { tank = 1.0, kbot = 1.0, hover = 1.0, ship = 1.0 } },
		[1] = { name = "Road", hardness = 1.0, receiveTracks = true, moveSpeeds = { tank = 1.0, kbot = 1.0, hover = 1.0, ship = 1.0 } },
		[2] = { name = "NoBuild", hardness = 1.0, receiveTracks = true, moveSpeeds = { tank = 1.0, kbot = 1.0, hover = 1.0, ship = 1.0 } },
		[3] = { name = "Water", hardness = 1.0, receiveTracks = true, moveSpeeds = { tank = 1.0, kbot = 1.0, hover = 1.0, ship = 1.0 } },
	},
}

return mapinfo
