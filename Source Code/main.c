/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

//void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
//{
//	if (GPIO_Pin == BUTTON_R_Pin)
//	{
//		uint8_t button_R_val = HAL_GPIO_ReadPin(BUTTON_R_GPIO_Port, BUTTON_R_Pin);
//		HAL_GPIO_WritePin(BLUE_LED_GPIO_Port, BLUE_LED_Pin, button_R_val);
//		uint8_t dataToSend = (button_R_val == GPIO_PIN_SET) ? '1' : '0'; // Convert to ASCII character
//		HAL_UART_Transmit(&huart2, &dataToSend, 1, 10); // Pass the address of dataToSend
//	}
//}

const int DEBOUNCE_DELAY = 150;
uint8_t send_data_R = 0;
uint8_t send_data_M = 0;
uint8_t send_data_L = 0;
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    static uint32_t last_time = 0;
    if (GPIO_Pin == BUTTON_R_Pin)
    {
        uint32_t now = HAL_GetTick(); // Get the current time in ms
        if (now - last_time > DEBOUNCE_DELAY) // Check if enough time has passed
        {
            last_time = now; // Update the time of the last accepted button press

            uint8_t button_R_val = HAL_GPIO_ReadPin(BUTTON_R_GPIO_Port, BUTTON_R_Pin);
            // Make sure the button is still pressed after the debounce delay
            if(button_R_val == GPIO_PIN_SET)
            {

                HAL_GPIO_WritePin(BLUE_LED_GPIO_Port, BLUE_LED_Pin, button_R_val);
                send_data_R = 1;
            }
        }
    }
        else
	if (GPIO_Pin == BUTTON_M_Pin)
		{
			uint32_t now = HAL_GetTick(); // Get the current time in ms
			if (now - last_time > DEBOUNCE_DELAY) // Check if enough time has passed
			{
				last_time = now; // Update the time of the last accepted button press

				uint8_t button_M_val = HAL_GPIO_ReadPin(BUTTON_M_GPIO_Port, BUTTON_M_Pin);
				// Make sure the button is still pressed after the debounce delay
				if(button_M_val == GPIO_PIN_SET)
				{

					HAL_GPIO_WritePin(RED_LED_GPIO_Port, RED_LED_Pin, button_M_val);
					send_data_M = 1;
				}
			}
		} else
		if (GPIO_Pin == BUTTON_L_Pin)
			{
				uint32_t now = HAL_GetTick(); // Get the current time in ms
				if (now - last_time > DEBOUNCE_DELAY) // Check if enough time has passed
				{
					last_time = now; // Update the time of the last accepted button press

					uint8_t button_L_val = HAL_GPIO_ReadPin(BUTTON_L_GPIO_Port, BUTTON_L_Pin);
					// Make sure the button is still pressed after the debounce delay
					if(button_L_val == GPIO_PIN_SET)
					{

						HAL_GPIO_WritePin(GREEN_LED_GPIO_Port, GREEN_LED_Pin, button_L_val);
						send_data_L = 1;
					}
				}
			}
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  if (send_data_R)
	  {
//          uint8_t dataToSend = '1'; // Send '1' for button press
//          HAL_UART_Transmit(&huart2, &dataToSend, 1, 10);
		  // Define the string to send
		  char dataToSend[] = "Button 1\n\r";
		  // Calculate the length of the string to send
		  size_t dataLength = sizeof(dataToSend) - 1; // Subtract 1 to exclude the null terminator for UART transmission
		  // Transmit the string over UART
		  HAL_UART_Transmit(&huart2, (uint8_t*)dataToSend, dataLength, 10);
          HAL_GPIO_WritePin(BLUE_LED_GPIO_Port, BLUE_LED_Pin, 0);
          send_data_R = 0;
	  }

	  if (send_data_M)
	  {
//          uint8_t dataToSend = '1'; // Send '1' for button press
//          HAL_UART_Transmit(&huart2, &dataToSend, 1, 10);
		  // Define the string to send
		  char dataToSend[] = "Button 2\n\r";
		  // Calculate the length of the string to send
		  size_t dataLength = sizeof(dataToSend) - 1; // Subtract 1 to exclude the null terminator for UART transmission
		  // Transmit the string over UART
		  HAL_UART_Transmit(&huart2, (uint8_t*)dataToSend, dataLength, 10);
          HAL_GPIO_WritePin(RED_LED_GPIO_Port, RED_LED_Pin, 0);
          send_data_M = 0;
	  }

	  if (send_data_L)
	  {
//          uint8_t dataToSend = '1'; // Send '1' for button press
//          HAL_UART_Transmit(&huart2, &dataToSend, 1, 10);
		  // Define the string to send
		  char dataToSend[] = "Button 3\n\r";
		  // Calculate the length of the string to send
		  size_t dataLength = sizeof(dataToSend) - 1; // Subtract 1 to exclude the null terminator for UART transmission
		  // Transmit the string over UART
		  HAL_UART_Transmit(&huart2, (uint8_t*)dataToSend, dataLength, 10);
          HAL_GPIO_WritePin(GREEN_LED_GPIO_Port, GREEN_LED_Pin, 0);
          send_data_L = 0;
	  }

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 50;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 9600;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOD, GREEN_LED_Pin|RED_LED_Pin|BLUE_LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : BUTTON_R_Pin BUTTON_L_Pin BUTTON_M_Pin */
  GPIO_InitStruct.Pin = BUTTON_R_Pin|BUTTON_L_Pin|BUTTON_M_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : GREEN_LED_Pin RED_LED_Pin BLUE_LED_Pin */
  GPIO_InitStruct.Pin = GREEN_LED_Pin|RED_LED_Pin|BLUE_LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
