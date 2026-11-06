// AA Example
import type { components } from "@/Api/OpenApi";

// General
export type ErrorSchema = components['schemas']['ErrorSchema']
export type ActionResponse = components['schemas']['ActionResponse']
export type MenuSchema = components['schemas']['MenuSchema']
export type ModalSchema = components['schemas']['ModalSchema']
export type UserData = components['schemas']['UserData']
export type UserSettingsSchema = components['schemas']['UserSettingsSchema']
export type UserSettingsUpdateRequest = components['schemas']['UserSettingsUpdateRequest']

// Character module
export type CharacterSchema = components['schemas']['CharacterSchema']
export type CharacterDetailSchema = components['schemas']['CharacterDetailSchema']
export type CharacterUpdateStatusSchema = components['schemas']['CharacterUpdateStatusSchema']
