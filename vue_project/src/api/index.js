import { get, post} from './http'

export const userLogin = p => post("/api/user/login",p)

export const drawTree = p => post('/draw/tree',p)

export const drawSingle = p => post('/draw/single',p)

export const drawOverlay = p => post('/draw/overlay',p)

export const drawWaveform = p => post('/draw/waveform',p)

export const drawGif = p => post('/draw/gif',p)

export const cardList = p => get('/home/card/list',p)

export const cardInfo = p => get('/home/card/info',p)

export const cardParamDefault = p => get('/home/card/parameters/defalt',p)

export const cardCopy = p => post('/home/card/copy',p)

export const cardUpdate = p => post('/home/card/update',p)

export const cardDelete = p => post('/home/card/delete',p)

export const createFlow = p => post('/home/card/create/flow',p)

export const createSub = p => post('/home/card/create/sub',p)

export const editStruct = p => get('/edit/struct',p)

export const editRun = p => post('/edit/run',p)

export const editSave = p => post('/edit/save',p)

export const editLog = p => get('/edit/log',p)

export const getFlowSubParams = p => get('/edit/flow/params',p)

export const updateFlowSubParams = p => post('/edit/flow/params/update',p)