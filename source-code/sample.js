import { Config } from '../config/config';
import apiFetcher from '../helpers/apiFetcher';
import { UserProfile, UserProfileUpdateInput, UserProfileLoaderInput } from '../types/userProfile.d';
import { ConnectionError, ErrorCauses, FetchError } from '../errors/index';
import UserProfileError from '../errors/invalidUserProfile';
import { StatusCodes, ErrorCodes, ErrorMessages } from '../errors/errorConstants';
import { Maybe } from '../types/maybe';

const generateUserProfileUrl = (userId: string): string => {
  return `${Config.config.apiEndpoint}/users/${userId}/profile`;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const handleUserProfileError = (error: any, userId: string, url: string, requestId: string) => {
  if (!(error instanceof FetchError)) {
    throw error;
  }
  const errorResponse = error?.response;
  switch (errorResponse?.status) {
    case 400:
      throw new UserProfileError(ErrorCodes.BAD_REQUEST, {
        statusCode: StatusCodes.BAD_REQUEST,
        value: [userId],
        field: ['userId'],
        requestId,
        userId,
        logAsInfo: true,
      });
    case 401:
      throw new UserProfileError(ErrorCodes.UNAUTHORIZED, {
        statusCode: StatusCodes.UNAUTHORIZED,
        value: [userId],
        field: ['userId'],
        requestId,
        userId,
        logAsInfo: true,
      });
    case 404:
      throw new UserProfileError(ErrorCodes.USER_NOT_FOUND, {
        statusCode: StatusCodes.USER_NOT_FOUND,
        value: [userId],
        field: ['userId'],
        requestId,
        userId,
        logAsInfo: true,
      });
    default:
      throw new ConnectionError(ErrorCauses.CONNECTION_PROBLEM, {
        statusCode: StatusCodes.CONNECTION_PROBLEM,
        errorDescription: ErrorMessages.API_CONNECTION_PROBLEM,
        requestId,
        userId,
        log: {
          system: 'userProfile',
          url,
        },
      });
  }
};

// eslint-disable-next-line consistent-return, @typescript-eslint/no-explicit-any
const fetchUserProfileData = async (userId: string, url: string, requestId: string): Promise<any> => {
  const payload = {
    method: 'GET',
    headers: {
      accept: 'application/json',
    },
  };
  try {
    const response = await apiFetcher.fetchData({
      url,
      payload,
      system: 'userProfile',
      requestId,
    });

    return response;
  } catch (error) {
    handleUserProfileError(error, userId, url, requestId);
  }
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const transformUserProfileResponse = async (response: any): Promise<UserProfile> => {
  const responseJSON = await response.json();

  const responseUserId = responseJSON?.userId;
  const responseUserName = responseJSON?.userName;
  const responseEmail = responseJSON?.email;
  const responseProfilePicture = responseJSON?.profilePicture || '';

  const userProfile: UserProfile = {
    userId: responseUserId,
    userName: responseUserName,
    email: responseEmail,
    profilePicture: responseProfilePicture,
  };

  return userProfile;
};

const retrieveUserProfile = async (
  userId: string,
  requestId: string,
): Promise<UserProfile> => {
  const url = generateUserProfileUrl(userId);
  const response = await fetchUserProfileData(userId, url, requestId);

  return transformUserProfileResponse(response);
};

const updateUserProfile = async (
  userId: string,
  updateInput: UserProfileUpdateInput,
  requestId: string,
): Promise<UserProfile> => {
  const url = generateUserProfileUrl(userId);
  const payload = {
    method: 'PUT',
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updateInput),
  };

  try {
    const response = await apiFetcher.fetchData({
      url,
      payload,
      system: 'userProfile',
      requestId,
    });

    return transformUserProfileResponse(response);
  } catch (error) {
    handleUserProfileError(error, userId, url, requestId);
  }
};

const loadUserProfiles = async (inputs: UserProfileLoaderInput[]): Promise<UserProfile[]> =>
  Promise.all(inputs.map((input) => retrieveUserProfile(input.userId, input.requestId)));

// eslint-disable-next-line import/prefer-default-export, @typescript-eslint/no-explicit-any
export const fetchUserProfilesFromLoader = (userIds: string[], context: any) =>
  context.Loader.load(loadUserProfiles, {
    userIds,
    requestId: context.requestId,
  });

export const updateUserProfiles = (userId: string, updateInput: UserProfileUpdateInput, context: any) =>
  context.Loader.load(async () => {
    return updateUserProfile(userId, updateInput, context.requestId);
  }, {
    userId,
    updateInput,
    requestId: context.requestId,
  });